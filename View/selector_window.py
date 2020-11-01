from PyQt5.QtWidgets import QWidget, QVBoxLayout
from lantz.qt import Frontend

from Backend.platina_backend import PlatinaBackend
from Drivers.camera_selector import CameraSelector
from Drivers.daq_selector import DaqSelector
from Drivers.fungen_selector import FungenSelector
from Drivers.lockin_selector import LockinSelector
from Drivers.motor_selector import MotorSelector


class SelectorWindow(Frontend):

    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        self.widget.setLayout(QVBoxLayout())
        self.setCentralWidget(self.widget)

        self.camera_selector = CameraSelector()
        self.daq_selector = DaqSelector()
        self.motor_selector = MotorSelector()
        self.lockin_selector = LockinSelector()
        self.fungen_selector = FungenSelector()

        self.widget.layout().addWidget(self.camera_selector)
        self.widget.layout().addWidget(self.daq_selector)
        self.widget.layout().addWidget(self.motor_selector)
        self.widget.layout().addWidget(self.lockin_selector)
        self.widget.layout().addWidget(self.fungen_selector)

    def camera(self):
        return self.camera_selector.camera()

    def daq(self):
        return self.daq_selector.daq()

    def lockin(self):
        return self.lockin_selector.lockin()

    def fungen(self):
        return self.fungen_selector.fungen()

    def dual_motor_backend(self) -> PlatinaBackend:
        """
            @brief returns the dual motor backend
            :return motor backend:
        """
        return self.motor_selector.motors()
