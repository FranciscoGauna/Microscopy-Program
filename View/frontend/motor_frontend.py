from PyQt5.QtCore import QTimer
from lantz.qt import Frontend
from Drivers.Motor.MotorDriver import Motor
from Backend.platina_backend import PlatinaBackend
from View.localization import locale


class MotorFrontend(Frontend):
    backend: Motor
    gui = ("UI", "motor_pos.ui")
    timer = QTimer()
    edge: str

    def __init__(self, edge, *args, **kwargs):
        self.edge = edge
        super().__init__(*args, **kwargs)


    def setupUi(self):
        super().setupUi()

        self.widget.motor_lb.setText(locale.get(self.edge + "_motor", "str_" + self.edge + "_motor"))

        self.widget.next_lb.setText(locale.get("next_pos", "str_next_pos"))
        self.widget.current_lb.setText(locale.get("current_pos", "str_current_pos"))
        self.widget.prev_lb.setText(locale.get("prev_pos", "str_prev_pos"))

    def connect_backend(self):
        super().connect_backend()

        self.widget.current_le.setText(str(self.backend.position()))
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

        self.motor_x_ft = MotorFrontend("x", backend=self.backend.motor_x())
        self.motor_y_ft = MotorFrontend("y", backend=self.backend.motor_y())
        self.widget.x_motor_lt.addWidget(self.motor_x_ft)
        self.widget.y_motor_lt.addWidget(self.motor_y_ft)

        self.widget.move_button.clicked.connect(self.move)

    def move(self):
        self.motor_x_ft.move_to()
        self.motor_y_ft.move_to()
