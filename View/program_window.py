from pathlib import Path
from threading import Thread

import cv2
from PyQt5.QtWidgets import QFileDialog

from lantz.qt.connect import connect_feat
from lantz.qt import Frontend, wrap_driver_cls
from PyQt5.QtWidgets import QErrorMessage

from Backend.camera_backend import CameraBackend
from Model.AnfatecDriver import AnfatecAMU24
from Model.MotorDriver import Motor, get_available_motors
from Backend.lockin_options import LockinControl
from Backend.platina_backend import PlatinaBackend
from Model.virtual_camera import VirtualCamera
from View.camera_window import CameraControlUi
from View.frontend.camera_only import CameraOnlyWindow
from View.frontend.camera_selector_frontend import CameraSelectorFrontend
from View.frontend.motor_frontend import DualMotorFrontend
from View.frontend.platina_frontend import PlatinaFrontend, MotorAlreadyOpenException
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
        self.widget.change_bt.pressed.connect(self.change_screen)

    def change_screen(self):
        try:
            self.platina_interface.open_motors()
        except MotorAlreadyOpenException:
            self.error_dialog = QErrorMessage()
            self.error_dialog.showMessage(locale.get("same_motor_exception", "str_same_motor_exception"))
            return

        camera = self.camera_interface.camera()
        camera = CameraBackend(camera)

        self.motor_interface = DualMotorFrontend(backend=self.platina_interface.backend)
        self.image_window = CameraOnlyWindow(backend=camera)

        self.widget.main_lt.removeWidget(self.platina_interface)
        self.platina_interface.close()
        self.platina_interface = None

        self.widget.main_lt.removeWidget(self.camera_interface)
        self.camera_interface.close()
        self.camera_interface = None

        #self.frequency_window = CameraControlUi(backend=camera)
        #self.widget.main_lt.addWidget(self.frequency_window)

        self.widget.main_lt.addWidget(self.motor_interface)
        self.image_window.show()
        self.image_window.closed_target = self
        self.camera_open = True

    def closeEvent(self, event):
        self.is_closing = True
        if self.image_window is not None:
            self.image_window.close()
        event.accept()

    def close_camera(self):
        if self.camera_open:
            self.widget.over_main_lt.addWidget(self.image_window)
            self.camera_open = False
