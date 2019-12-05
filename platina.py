from Model.MotorDriver import Motor
from Backend.platina_backend import PlatinaBackend
from View.frontend.platina_frontend import PlatinaFrontend
from lantz.core.log import log_to_screen, INFO
from lantz.qt import start_gui_app, wrap_driver_cls


log_to_screen(INFO)

QMotor = wrap_driver_cls(Motor)


with QMotor() as motor_x, QMotor() as motor_y:
    backend = PlatinaBackend(motor_x, motor_y)
    start_gui_app(backend, PlatinaFrontend)
    pass
