from Backend.lockin_backend import LockinBackend
from Backend.platina_backend import PlatinaBackend
from Drivers.Lockin.anfatec_driver import VirtualLockin
from Drivers.Motor.MotorDriver import Motor
from View.frontend.point_list import OperationList


class TestLockin(VirtualLockin):

    def __init__(self, filename):
        pass


def run():
    platina_backend = PlatinaBackend(Motor(), Motor())
    platina_backend.set_motor_x("virtual")
    platina_backend.set_motor_y("virtual")
    point_list_ft = OperationList(backend=[])
    lockin_backend = LockinBackend(lockin=TestLockin(""))
    # experiment_worker = ExperimentWorker(point_list_ft, platina_backend, lockin_backend)
    # experiment_tab = ExperimentTab(backend=experiment_worker)

