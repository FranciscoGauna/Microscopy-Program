from PyQt5.QtWidgets import QFileDialog
from lantz.qt import Frontend, wrap_driver_cls
from Backend.platina_backend import PlatinaBackend
from Drivers.Motor.MotorDriver import Motor
from View.localization import locale
from pathlib import Path


class MotorSelector(Frontend):
    backend: PlatinaBackend
    gui = ("ui", "motor_selector.ui")
    conf_x = None
    conf_y = None

    def __init__(self):
        super().__init__()

        q_motor = wrap_driver_cls(Motor)
        motor_x = q_motor()
        motor_y = q_motor()
        self.backend = PlatinaBackend(motor_x, motor_y)

        motors = self.backend.motors
        for element in motors:
            self.widget.x_cb.addItem(element)
            self.widget.y_cb.addItem(element)

        self.widget.x_file_button.pressed.connect(self.load_x)
        self.widget.y_file_button.pressed.connect(self.load_y)

    def setupUi(self):
        super().setupUi()

        self.widget.x_label.setText(locale.get("x_motor", "str_x_motor"))
        self.widget.y_label.setText(locale.get("y_motor", "str_y_motor"))

        self.widget.x_file_button.setText(locale.get("load_conf_file", "str_load_conf_file"))
        self.widget.y_file_button.setText(locale.get("load_conf_file", "str_load_conf_file"))

    def load_x(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "Configuration File (*.cfg);;All Files (*)", options=options)
        if file_name:
            self.widget.x_file_button.setText(Path(file_name).name)
            self.conf_x = open(file_name, "r+")

    def load_y(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "Configuration File (*.cfg);;All Files (*)", options=options)
        if file_name:
            self.widget.y_file_button.setText(Path(file_name).name)
            self.conf_y = open(file_name, "r+")

    def open_motors(self):
        if self.widget.x_cb.currentText() == self.widget.y_cb.currentText()\
                and self.widget.x_cb.currentText() != "virtual":
            raise MotorAlreadyOpenException
        self.backend.set_motor_x(self.backend.motors[self.widget.x_cb.currentText()], self.conf_x)
        self.backend.set_motor_y(self.backend.motors[self.widget.y_cb.currentText()], self.conf_y)

    def motors(self):
        self.open_motors()
        return self.backend


class MotorAlreadyOpenException(Exception):
    pass
