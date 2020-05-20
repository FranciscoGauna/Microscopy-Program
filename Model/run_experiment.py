import traceback
import os
from math import sqrt
from time import sleep
from copy import deepcopy
from datetime import datetime

from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtGui import QImage, QColor

from Backend.lockin_options import LockinBackend
from Backend.platina_backend import PlatinaBackend
from Model.operation import Operation
from Model.scaler import lin_list, square_list
from View.localization import locale
from magic_numbers import pixel_to_counts_factor, spectrum_n


class ExperimentWorker(QThread):
    step = 0
    total = 1
    results = []
    current_operation: Operation

    max: float
    min: float
    color_list_base = square_list(0, 255, spectrum_n)
    color_list = []
    color_value_list = []
    qimage = QImage(1, 1, QImage.Format_RGB32)
    points: list

    def __init__(self, operation_list: list, platina: PlatinaBackend, lockin: LockinBackend, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.operation_list = operation_list
        self.platina = platina
        self.lockin = lockin

        # Initialization of the color spectrum and the image
        self.spectrum_n = spectrum_n
        for i in range(self.spectrum_n):
            color = QColor()
            color.setRgb(self.color_list_base[i], 255, 0)
            self.color_list.append(color)
        for i in reversed(range(0, self.spectrum_n - 1)):
            color = QColor()
            color.setRgb(255, self.color_list_base[i], 0)
            self.color_list.append(color)

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        try:
            self.results = []
            operation_list = deepcopy(self.operation_list)
            point_list = []
            for operation in operation_list:
                point_list.extend(operation.to_points())

            self.total = len(point_list)
            operation_end = 0
            operation_index = -1
            time = datetime.now()
            results_filename = time.isoformat().replace(":", "-").replace("T", " ").split(".")[0] + ".dat"
            directory = 'Results'
            if os.path.isdir(directory):
                results_filename = os.path.join(directory, results_filename)
            results_file = open(results_filename, "w+")
            for i in range(0, self.total):
                if i >= operation_end:
                    operation_index += 1
                    self.current_operation = operation_list[operation_index]
                    operation_end += len(self.current_operation.to_points())

                    self.qimage = QImage(self.current_operation.width(), self.current_operation.height(),
                                         QImage.Format_RGB32)
                    self.qimage.fill(QColor(0, 0, 0))
                    self.points = []
                    self.max = self.min = self.lockin.get_amplitude()
                    self.create_colors()

                self.step = i
                point = point_list[i]
                x_count = point.x * pixel_to_counts_factor
                y_count = point.y * pixel_to_counts_factor
                self.platina.move_to(x_count, y_count)
                while not self.platina.stopped(time):
                    sleep(0.01)
                value = self.lockin.get_amplitude()
                result = [x_count, y_count, point.frequency, value, point.display_x, point.display_y]
                self.results.append(result)
                self.load_pixel(point.display_x, point.display_y, value)
                results_file.write(str(result))
                results_file.write("\n")
            self.step += 1
            print(datetime.now() - time)
            results_file.close()
        except:
            traceback.print_exc()

    # Aca empiezan el codigo del color
    def load_pixel(self, x, y, value):
        try:
            if value > self.max:
                self.max = value
                self.create_colors()
                self.recalculate_colors()
            if value < self.min:
                self.min = value
                self.create_colors()
                self.recalculate_colors()

            color = self.decide_color(value)
            self.points.append([x, y, value, color])
            self.qimage.setPixelColor(x, y, color)
        except:
            traceback.print_exc()

    def create_colors(self):
        result = []
        value_list = lin_list(self.min, self.max, self.spectrum_n * 2)
        for i in range(0, (self.spectrum_n * 2) - 1):
            result.append((value_list[i + 1], self.color_list[i]))
        self.color_value_list = result

    def decide_color(self, value):
        i = 0
        length = len(self.color_value_list)
        while i < length and value > self.color_value_list[i][0]:
            i += 1
        if i == length:
            i = length - 1
        return self.color_value_list[i][1]

    def recalculate_colors(self):
        for point in self.points:
            x = point[0]
            y = point[1]
            value = point[2]
            point[3] = self.decide_color(value)
            self.qimage.setPixelColor(x, y, point[3])


class ProgressBarController:
    exp_worker: ExperimentWorker
    gui = ("UI", "exp_progress.ui")
    timer = QTimer()

    def __init__(self, progress_bar, exp_button, exp_worker: ExperimentWorker, current_le):
        self.exp_worker = exp_worker
        self.exp_button = exp_button
        self.progress_bar = progress_bar
        self.current_le = current_le
        self.progress_bar.setFormat("%v/%m")
        self.exp_button.setText(locale.get("run_exp", "str_run_exp"))
        self.progress_bar.setRange(0, self.exp_worker.total)
        self.exp_button.pressed.connect(self.start)

    def start(self):
        if self.exp_worker.isRunning():
            return
        if len(self.exp_worker.operation_list) == 0:
            return

        self.exp_worker.start()
        self.progress_bar.setRange(0, self.exp_worker.total)

        if not self.timer.isActive():
            self.timer.timeout.connect(self.load_value)
            self.timer.setInterval(15)
            self.timer.start()

    def load_value(self):
        try:
            self.progress_bar.setValue(self.exp_worker.step)
            self.progress_bar.setRange(0, self.exp_worker.total)
            if len(self.exp_worker.results) > 0:
                self.current_le.setText(str(self.exp_worker.results[-1]))
        except:
            traceback.print_exc()

    def qimage(self):
        return self.exp_worker.qimage
