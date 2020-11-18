from lantz.qt import Frontend

from Backend.experiment_backend import ExperimentBackend
from Backend.frequency_backend import FrequencyController
from Backend.lockin_backend import LockinBackend
from View.frontend.FrequencyStepFrontend import FrequencyStepFrontend
from View.frontend.camera_control_ui import ImageDrawerFt
from View.frontend.experiment_tab import ExperimentTab
from View.frontend.lockin_options import LockinOptions
from View.frontend.lockin_pll import LockinPll
from View.frontend.lockin_tab import LockinTab
from View.frontend.motor_frontend import DualMotorFrontend
from View.frontend.offset_frontend import OffsetFrontend
from View.frontend.point_list import OperationList
from Model.run_experiment import ExperimentWorker
from View.localization import locale


class TabsFrontend(Frontend):
    gui = ("frontend", "UI", "conf_tabs.ui")

    frequency_ft: FrequencyStepFrontend
    operation_list_ft: OperationList
    point_gen_ft: ImageDrawerFt

    lockin_backend: LockinBackend
    lockin_options: LockinOptions
    lockin_pll: LockinPll

    def __init__(self, image, lockin, motor_backend, focus_backend, fungen):
        super().__init__()

        lockin_backend = LockinBackend(lockin=lockin)
        self.lockin_tab = LockinTab(backend=lockin_backend)

        self.widget.lockin_tab_lt.addWidget(self.lockin_tab)

        self.widget.motor_tab_lt.addWidget(DualMotorFrontend(backend=motor_backend), 1, 1)

        freq_backend = FrequencyController()
        self.frequency_ft = FrequencyStepFrontend(backend=freq_backend)
        self.operation_list_ft = OperationList(backend=[])
        self.point_gen_ft = ImageDrawerFt(self.operation_list_ft, self.frequency_ft, image)

        self.offset_ft = OffsetFrontend(self.point_gen_ft)

        self.widget.top_c_lt.addWidget(self.point_gen_ft)
        self.widget.top_c_lt.addWidget(self.frequency_ft)
        self.widget.top_c_lt.addWidget(self.offset_ft)
        self.widget.bot_c_lt.addWidget(self.operation_list_ft)

        experiment_worker = ExperimentWorker(self.operation_list_ft.operation_list, motor_backend, lockin_backend,
                                             focus_backend, fungen)
        experiment_backend = ExperimentBackend(worker=experiment_worker)
        self.experiment_tab = ExperimentTab(backend=experiment_backend)
        self.widget.experiment_lt.addWidget(self.experiment_tab)

    def setupUi(self):
        self.widget.main_program_tabs.setTabText(0, locale.get("lockin_configuration", "str_lockin_configuration"))
        self.widget.main_program_tabs.setTabText(1, locale.get("sample_alignment", "str_sample_alignment"))
        self.widget.main_program_tabs.setTabText(2, locale.get("protocol_selection", "str_protocol_selection"))
        self.widget.main_program_tabs.setTabText(3, locale.get("thermal_imaging", "str_thermal_imaging"))
