from lantz.qt import Backend
from lantz.core import Feat
from Model.MotorDriver import Motor, get_available_motors


class PlatinaBackend(Backend):
    motors = get_available_motors()
    motors["virtual"] = "virtual"

    def __init__(self, motor_x: Motor, motor_y: Motor):
        super().__init__()
        self._motor_x = motor_x
        self._motor_y = motor_y

    def motor_x(self):
        return self._motor_x

    def set_motor_x(self, motor, conf):
        self._motor_x.open_motor(motor, conf)

    def motor_x_name(self):
        return self._motor_x.current_motor()

    def motor_y(self):
        return self._motor_y

    def set_motor_y(self, motor, conf):
        self._motor_y.open_motor(motor, conf)

    def motor_y_name(self):
        return self._motor_y.current_motor()
