from lantz.qt import Backend
from lantz.core import Feat
from Model.MotorDriver import Motor, get_available_motors


class PlatinaBackend(Backend):

    def __init__(self, motor_x: Motor, motor_y: Motor):
        super().__init__()
        self._motor_x = motor_x
        self._motor_y = motor_y

    @Feat(values=get_available_motors())
    def motor_x(self):
        return self._motor_x.current_motor()

    @motor_x.setter
    def motor_x(self, motor):
        self._motor_x.open_motor(motor)
