from pathlib import Path
from threading import Thread

import cv2
from PyQt5.QtWidgets import QFileDialog, QPushButton

from lantz.qt.connect import connect_feat
from lantz.qt import Frontend, wrap_driver_cls
from PyQt5.QtWidgets import QErrorMessage

from Backend.camera_backend import CameraBackend
from Backend.frequency_backend import FrequencyController
from Model.AnfatecDriver import AnfatecAMU24
from Model.MotorDriver import Motor, get_available_motors
from Backend.lockin_options import LockinControl
from Backend.platina_backend import PlatinaBackend
from Model.frequency_scan import frequency_scanner_point
from Model.virtual_camera import VirtualCamera
from View.camera_window import CameraControlUi
from View.frontend.FrequencyStepFrontend import FrequencyStepFrontend
from View.frontend.camera_control_ui import ImageDrawerFt
from View.frontend.camera_only import CameraOnlyWindow
from View.frontend.camera_selector_frontend import CameraSelectorFrontend
from View.frontend.motor_frontend import DualMotorFrontend
from View.frontend.platina_frontend import PlatinaFrontend, MotorAlreadyOpenException
from View.frontend.point_list import PointList
from View.frontend.show_data import ExperimentWorker, ExperimentRunner
from View.localization import locale

from View.lockin_window import LockinControlUi
from lantz.qt.app import start_gui_app


class MainFrontend(Frontend):
    backend: PlatinaBackend
    gui = ("frontend", "UI", "main.ui")
    lost_thread = Thread()
    is_closing = False
    image_window = None
    camera_open = False

    point_list_frontend: PointList
    frequency_frontend: FrequencyStepFrontend

    def setupUi(self):
        super().setupUi()
        self.widget.change_bt.setText(locale.get("load", "str_load"))

    def connect_backend(self):
        super().connect_backend()

        QMotor = wrap_driver_cls(Motor)
        motor_x = QMotor()
        motor_y = QMotor()
        backend = PlatinaBackend(motor_x, motor_y)
        self.camera_interface = CameraSelectorFrontend()
        self.widget.main_lt.addWidget(self.camera_interface)
        self.platina_interface = PlatinaFrontend(backend=backend)
        self.widget.main_lt.addWidget(self.platina_interface)
        self.
        self.widget.main_lt.addWidget
        self.widget.change_bt.pressed.connect(self.change_screen)

    def change_screen(self):
        if self.image_window is not None:
            return

        try:
            self.platina_interface.open_motors()
        except MotorAlreadyOpenException:
            self.error_dialog = QErrorMessage()
            self.error_dialog.showMessage(locale.get("same_motor_exception", "str_same_motor_exception"))
            return

        self.camera = self.camera_interface.camera()
        self.camera = CameraBackend(self.camera)

        self.widget.change_bt.pressed.connect(self.toggle_camera)

        self.motor_interface = DualMotorFrontend(backend=self.platina_interface.backend)
        self.image_window = CameraOnlyWindow(backend=self.camera)

        self.widget.main_lt.removeWidget(self.platina_interface)
        self.platina_interface.close()
        self.platina_interface = None

        self.widget.main_lt.removeWidget(self.camera_interface)
        self.camera_interface.close()
        self.camera_interface = None

        self.camera_open = True

        freq_backend = FrequencyController()
        self.frequency_frontend = FrequencyStepFrontend(backend=freq_backend)
        self.point_list_frontend = PointList(backend=[])
        self.point_gen_ft = ImageDrawerFt(self.point_list_frontend, self.frequency_frontend, self.image_window.image)

        self.toggle_camera()

        self.widget.main_lt.addWidget(self.point_gen_ft, 0, 0)
        self.widget.main_lt.addWidget(self.frequency_frontend, 1, 0)
        self.widget.main_lt.addWidget(self.point_list_frontend, 0, 1)
        self.widget.main_lt.addWidget(self.motor_interface, 1, 1)

        experiment_worker = ExperimentWorker(self.point_list_frontend, self.motor_interface.backend)
        self.experiment_ft = ExperimentRunner(backend=experiment_worker)
        self.widget.bt_lt.insertWidget(0, self.experiment_ft)

    def closeEvent(self, event):
        self.is_closing = True
        if self.image_window is not None:
            self.image_window.close()
        event.accept()

    def toggle_camera(self):
        if self.camera_open:

            self.widget.over_main_lt.addWidget(self.image_window)
            self.camera_open = False
            self.image_window.closed_target = None

            self.widget.change_bt.setText(locale.get("pop_out_camera", "str_pop_out_camera"))
        else:
            self.widget.over_main_lt.removeWidget(self.image_window)
            new_image = CameraOnlyWindow(backend=self.camera)
            self.image_window.image.new_image_data(new_image.image)
            self.point_gen_ft.connect_image(new_image.image)

            self.image_window.deleteLater()
            self.image_window = new_image
            self.image_window.show()
            self.image_window.closed_target = self
            self.camera_open = True

            self.widget.change_bt.setText(locale.get("close_camera", "str_close_camera"))

