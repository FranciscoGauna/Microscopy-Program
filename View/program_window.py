from lantz.qt import Frontend, wrap_driver_cls
from PyQt5.QtWidgets import QErrorMessage

from Model.MotorDriver import Motor
from Backend.camera_backend import CameraBackend
from Backend.frequency_backend import FrequencyController
from Backend.lockin_options import LockinBackend
from Backend.platina_backend import PlatinaBackend
from View.frontend.FrequencyStepFrontend import FrequencyStepFrontend
from View.frontend.camera_control_ui import ImageDrawerFt
from View.frontend.camera_only import CameraOnlyWindow
from View.frontend.camera_selector_frontend import CameraSelectorFrontend
from View.frontend.lockin_options import LockinOptions
from View.frontend.lockin_pll import LockinPll
from View.frontend.motor_frontend import DualMotorFrontend
from View.frontend.platina_frontend import MotorSelector, MotorAlreadyOpenException
from View.frontend.point_list import OperationList
from View.frontend.select_lockin import LockinSelector
from View.frontend.run_experiment import ExperimentWorker, ExperimentRunner
from View.localization import locale
from View.main_tabs import TabsFrontend


class MainFrontend(Frontend):
    backend: PlatinaBackend
    gui = ("frontend", "UI", "main.ui")
    initialized = False
    is_closing = False
    image_ft = None
    camera_open = False

    # First screen
    camera_selector: CameraSelectorFrontend
    motor_selector: MotorSelector
    lockin_selector: LockinSelector
    error_dialog: QErrorMessage

    # Second screen
    camera_bc: CameraBackend
    point_gen_ft: ImageDrawerFt
    tab_frontend: TabsFrontend

    def setupUi(self):
        super().setupUi()
        self.widget.change_bt.setText(locale.get("load", "str_load"))

    def connect_backend(self):
        super().connect_backend()

        q_motor = wrap_driver_cls(Motor)
        motor_x = q_motor()
        motor_y = q_motor()
        backend = PlatinaBackend(motor_x, motor_y)
        self.camera_selector = CameraSelectorFrontend()
        self.widget.main_lt.addWidget(self.camera_selector)
        self.motor_selector = MotorSelector(backend=backend)
        self.widget.main_lt.addWidget(self.motor_selector)
        self.lockin_selector = LockinSelector()
        self.widget.main_lt.addWidget(self.lockin_selector)
        self.widget.change_bt.pressed.connect(self.change_screen)

    def change_screen(self):
        if self.initialized:
            return
        try:
            self.motor_selector.open_motors()
        except MotorAlreadyOpenException:
            self.error_dialog = QErrorMessage()
            self.error_dialog.showMessage(locale.get("same_motor_exception", "str_same_motor_exception"))
            return

        self.initialized = True

        camera = self.camera_selector.camera()
        self.camera_bc = CameraBackend(camera)
        self.image_ft = CameraOnlyWindow(backend=self.camera_bc)
        self.widget.main_lt.removeWidget(self.camera_selector)
        self.camera_selector.close()
        delattr(self, "camera_selector")

        motor_interface = DualMotorFrontend(backend=self.motor_selector.backend)
        self.widget.main_lt.removeWidget(self.motor_selector)
        self.motor_selector.close()
        delattr(self, "motor_selector")

        lockin = self.lockin_selector.open_lockin()
        self.widget.main_lt.removeWidget(self.lockin_selector)
        self.lockin_selector.close()
        delattr(self, "lockin_selector")

        self.widget.change_bt.pressed.connect(self.toggle_camera)
        self.camera_open = True
        self.toggle_camera()

        self.tab_frontend = TabsFrontend(self.image_ft.image, lockin, motor_interface)
        self.point_gen_ft = self.tab_frontend.point_gen_ft
        self.widget.main_lt.addWidget(self.tab_frontend)

    def closeEvent(self, event):
        self.is_closing = True
        if self.image_ft is not None:
            self.image_ft.close()
        event.accept()

    def toggle_camera(self):
        if self.camera_open:
            self.widget.over_main_lt.addWidget(self.image_ft)
            self.camera_open = False
            self.image_ft.closed_target = None
            self.widget.change_bt.setText(locale.get("pop_out_camera", "str_pop_out_camera"))
        else:
            self.widget.over_main_lt.removeWidget(self.image_ft)
            new_image = CameraOnlyWindow(backend=self.camera_bc)
            self.image_ft.image.new_image_data(new_image.image)
            self.point_gen_ft.connect_image(new_image.image)
            self.image_ft.deleteLater()
            self.image_ft = new_image
            self.image_ft.show()
            self.image_ft.closed_target = self
            self.camera_open = True
            self.widget.change_bt.setText(locale.get("pop_in_camera", "str_pop_in_camera"))
