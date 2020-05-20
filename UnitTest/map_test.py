from Backend.lockin_options import LockinBackend
from Backend.platina_backend import PlatinaBackend
from Model.AnfatecDriver import VirtualLockin
from Model.MotorDriver import Motor
from View.frontend.experiment_tab import ExperimentTab
from View.frontend.point_list import OperationList
from Model.run_experiment import ExperimentWorker


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

