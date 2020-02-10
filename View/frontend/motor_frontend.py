from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QSpinBox
from lantz.qt import Frontend
from lantz.qt.connect import connect_feat
from Model.MotorDriver import Motor, get_available_motors
from Backend.platina_backend import PlatinaBackend
from View.localization import locale
from pathlib import Path


class MotorFrontend(Frontend):
    backend: Motor
    gui = ("UI", "motor_pos.ui")
    timer = QTimer()

    def setupUi(self):
        super().setupUi()

    def connect_backend(self):
        super().connect_backend()

        self.widget.next_lb.setText(locale.get("next_pos", "str_next_pos"))

        self.widget.current_lb.setText(locale.get("current_pos", "str_current_pos"))
        self.widget.current_le.setText(str(self.backend.position()))

        self.widget.prev_lb.setText(locale.get("prev_pos", "str_prev_pos"))
        self.widget.prev_le.setText(str(self.backend.position()))

        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def move_to(self):
        self.widget.prev_le.setText(self.widget.current_le.text())
        self.backend.move_to(self.widget.next_sb.value())

    def update(self):
        self.widget.current_le.setText(str(self.backend.position()))

class DualMotorFrontend(Frontend):
    backend: PlatinaBackend
    motor_x_ft: MotorFrontend
    motor_y_ft: MotorFrontend
    gui = ("UI", "dual_motor.ui")

    def setupUi(self):
        super().setupUi()

    def connect_backend(self):
        super().connect_backend()

        self.motor_x_ft = MotorFrontend(backend=self.backend.motor_x())
        self.motor_y_ft = MotorFrontend(backend=self.backend.motor_y())
        self.widget.x_motor_lt.addWidget(self.motor_x_ft)
        self.widget.y_motor_lt.addWidget(self.motor_y_ft)

        self.widget.move_button.clicked.connect(self.move)

    def move(self):
        self.motor_x_ft.move_to()
        self.motor_y_ft.move_to()
