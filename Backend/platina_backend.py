from datetime import timedelta, datetime

from lantz.qt import Backend
from Drivers.Motor.MotorDriver import Motor, get_available_motors


class PlatinaBackend(Backend):
    motors = get_available_motors()
    motors["virtual"] = "virtual"

    _status_time = datetime.now()
    _status_interval = timedelta(milliseconds=10)

    def __init__(self, motor_x: Motor, motor_y: Motor):
        super().__init__()
        self._motor_x = motor_x
        self._motor_y = motor_y

    def motor_x(self):
        return self._motor_x

    def set_motor_x(self, motor, conf=None):
        self._motor_x.open_motor(motor, conf)

    def motor_x_name(self):
        return self._motor_x.current_motor()

    def motor_y(self):
        return self._motor_y

    def set_motor_y(self, motor, conf=None):
        self._motor_y.open_motor(motor, conf)

    def motor_y_name(self):
        return self._motor_y.current_motor()

    def move_to(self, x, y):
        self._motor_x.move_to(x)
        self._motor_y.move_to(y)

    def stopped(self, debug_time=datetime.now()):
        x_stopped = self._motor_x.stopped()
        #print(datetime.now() - debug_time)
        #print(x_stopped)
        y_stopped = self._motor_y.stopped()
        #print(datetime.now() - debug_time)
        #print(y_stopped)
        return x_stopped and y_stopped
