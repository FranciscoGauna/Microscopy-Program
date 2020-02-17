from lantz.qt import Frontend

from Backend.frequency_backend import FrequencyController
from Backend.lockin_options import LockinControl
from View.frontend.FrequencyStepFrontend import FrequencyStepFrontend
from View.frontend.camera_control_ui import ImageDrawerFt
from View.frontend.lockin_options import LockinOptions
from View.frontend.lockin_pll import LockinPll
from View.frontend.offset_frontend import OffsetFrontend
from View.frontend.point_list import OperationList
from View.frontend.run_experiment import ExperimentWorker, ExperimentRunner


class TabsFrontend(Frontend):
    gui = ("frontend", "UI", "conf_tabs.ui")

    frequency_ft: FrequencyStepFrontend
    point_list_ft: OperationList
    point_gen_ft: ImageDrawerFt

    lockin_backend: LockinControl
    lockin_options: LockinOptions
    lockin_pll: LockinPll

    experiment_ft: ExperimentRunner

    def __init__(self, image, lockin, motor_interface):
        super().__init__()

        self.lockin_backend = LockinControl(lockin=lockin)
        self.lockin_options = LockinOptions(backend=self.lockin_backend)
        self.lockin_pll = LockinPll(backend=self.lockin_backend)

        self.widget.motor_tab_lt.addWidget(motor_interface, 1, 1)

        freq_backend = FrequencyController()
        self.frequency_ft = FrequencyStepFrontend(backend=freq_backend)
        self.point_list_ft = OperationList(backend=[])
        self.point_gen_ft = ImageDrawerFt(self.point_list_ft, self.frequency_ft, image)

        self.offset_ft = OffsetFrontend(self.point_gen_ft)

        self.widget.top_c_lt.addWidget(self.point_gen_ft)
        self.widget.top_c_lt.addWidget(self.frequency_ft)
        self.widget.top_c_lt.addWidget(self.offset_ft)
        self.widget.bot_c_lt.addWidget(self.point_list_ft)

        experiment_worker = ExperimentWorker(self.point_list_ft, motor_interface.backend, self.lockin_backend)
        self.experiment_ft = ExperimentRunner(backend=experiment_worker)
