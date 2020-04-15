import traceback
from time import sleep
from copy import deepcopy
from datetime import datetime

from lantz.qt import Frontend
from PyQt5.QtCore import QThread, QTimer

from Backend.lockin_options import LockinBackend
from Backend.platina_backend import PlatinaBackend
from Model.operation import Operation
from View.localization import locale
from magic_numbers import pixel_to_counts_factor


class ExperimentWorker(QThread):
    step = 0
    total = 1
    results = []
    current_operation: Operation

    def __init__(self, operation_list: list, platina: PlatinaBackend, lockin: LockinBackend, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.operation_list = operation_list
        self.platina = platina
        self.lockin = lockin

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        try:
            self.results = []
            point_list = []
            operation_list = []
            for element in self.operation_list:
                operation_list.append(element)
            for operation in operation_list:
                point_list.extend(operation.to_points())
            self.total = len(point_list)
            operation_end = 0
            operation_index = -1
            time = datetime.now()
            results_filename = time.isoformat().replace(":", "-").replace("T", " ").split(".")[0] + ".dat"
            for i in range(0, self.total):
                if i >= operation_end:
                    operation_index += 1
                    self.current_operation = operation_list[operation_index]
                    operation_end += len(self.current_operation.to_points())
                self.step = i
                point = point_list[i]
                x_count = point.x * pixel_to_counts_factor
                y_count = point.y * pixel_to_counts_factor
                self.platina.move_to(x_count, y_count)
                while not self.platina.stopped(time):
                    sleep(0.01)
                self.results.append([x_count, y_count, self.lockin.get_amplitude()])
            self.step += 1
            print(datetime.now()-time)
            results_file = open(results_filename, "w+")
            for result in self.results:
                results_file.write(str(result))
                results_file.write("\n")
            results_file.close()

        except:
            traceback.print_exc()


class ProgressBarController:
    backend: ExperimentWorker
    gui = ("UI", "exp_progress.ui")
    timer = QTimer()

    def __init__(self, progress_bar, exp_button, exp_worker, current_le):
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
            self.current_le.setText(str(self.exp_worker.results[-1]))
        except:
            traceback.print_exc()
