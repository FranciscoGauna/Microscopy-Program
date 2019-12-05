from lantz.qt import Frontend
from lantz.qt.connect import connect_feat
from Model.MotorDriver import Motor, get_available_motors
from View.localization import locale


class PlatinaFrontend(Frontend):
    backend: Motor
    gui = ("UI", "select_motors_interface.ui")

    def setupUi(self):
        super().setupUi()

    def connect_backend(self):
        super().connect_backend()
        connect_feat(self.widget.x_cb, self.backend, "motor_x")
