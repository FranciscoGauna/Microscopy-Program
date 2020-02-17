from time import sleep
from copy import deepcopy
from datetime import datetime

from lantz.qt import Frontend
from PyQt5.QtCore import QThread, QTimer

from Backend.lockin_options import LockinControl
from Backend.platina_backend import PlatinaBackend
from View.localization import locale
from magic_numbers import pixel_to_counts_factor


class ExperimentWorker(QThread):
    step = 0
    total = 1

    def __init__(self, point_list_ft, platina: PlatinaBackend, lockin: LockinControl, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.point_list_ft = point_list_ft
        self.platina = platina
        self.lockin = lockin

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        point_list = []
        for operation in self.point_list_ft.point_list:
            point_list.extend(operation.to_points())
        self.total = len(point_list)
        time = datetime.now()
        for i in range(0, self.total):
            self.step = i
            point = point_list[i]
            x_count = point.x * pixel_to_counts_factor
            y_count = point.y * pixel_to_counts_factor
            self.platina.move_to(x_count, y_count)
            while not self.platina.stopped(time):
                sleep(0.01)
            self.lockin.get_amplitude()
        self.step += 1
        print(datetime.now()-time)


class ExperimentRunner(Frontend):
    backend: ExperimentWorker
    gui = ("UI", "exp_progress.ui")
    timer = QTimer()

    def setupUi(self):
        self.widget.exp_progress.setFormat("%v/%m")
        self.widget.run_button.setText(locale.get("run_exp", "str_run_exp"))

    def connect_backend(self):
        self.widget.exp_progress.setRange(0, self.backend.total)
        self.widget.run_button.pressed.connect(self.start)

    def start(self):
        if self.backend.isRunning():
            return

        self.backend.start()
        self.widget.exp_progress.setRange(0, self.backend.total)

        if not self.timer.isActive():
            self.timer.timeout.connect(self.load_value)
            self.timer.setInterval(15)
            self.timer.start()

    def load_value(self):
        self.widget.exp_progress.setValue(self.backend.step)
        self.widget.exp_progress.setRange(0, self.backend.total)
