import sys
import traceback
from PyQt5.QtWidgets import QErrorMessage, QPushButton
from lantz.qt import Frontend, wrap_driver_cls

from Backend.camera_backend import CameraBackend
from Backend.focus_backend import FocusBackend
from Backend.platina_backend import PlatinaBackend
from Drivers.Motor.MotorDriver import Motor
from View.frontend.camera_control_ui import ImageDrawerFt
from View.frontend.camera_only import CameraOnlyWindow
from Drivers.camera_selector import CameraSelectorFrontend
from Drivers.daq_selector import DaqSelectorFrontend
from View.frontend.focus_frontend import FocusFrontend
from View.frontend.motor_frontend import DualMotorFrontend
from Drivers.motor_selector import MotorSelector, MotorAlreadyOpenException
from Drivers.lockin_selector import LockinSelector
from View.localization import locale
from View.main_tabs import TabsFrontend


class MainFrontend(Frontend):
    backend: PlatinaBackend
    gui = ("frontend", "UI", "main.ui")
    initialized = False
    is_closing = False
    image_ft = None
    camera_popped = False
    camera_open = True

    # First
    daq_selector: DaqSelectorFrontend
    camera_selector: CameraSelectorFrontend
    motor_selector: MotorSelector
    lockin_selector: LockinSelector
    error_dialog: QErrorMessage

    # Second screen
    camera_bc: CameraBackend
    point_gen_ft: ImageDrawerFt
    tab_frontend: TabsFrontend
    focus_frontend: FocusFrontend

    def setupUi(self):
        super().setupUi()
        self.widget.change_bt.setText(locale.get("load", "str_load"))

    def connect_backend(self):
        super().connect_backend()

        # DAQ
        self.daq_selector = DaqSelectorFrontend()
        self.widget.main_lt.addWidget(self.daq_selector)

        # Camera
        self.camera_selector = CameraSelectorFrontend()
        self.widget.main_lt.addWidget(self.camera_selector)

        # Motor
        q_motor = wrap_driver_cls(Motor)
        motor_x = q_motor()
        motor_y = q_motor()
        motor_backend = PlatinaBackend(motor_x, motor_y)
        self.motor_selector = MotorSelector(backend=motor_backend)
        self.widget.main_lt.addWidget(self.motor_selector)

        # Lockin
        self.lockin_selector = LockinSelector()
        self.widget.main_lt.addWidget(self.lockin_selector)

        self.widget.change_bt.clicked.connect(self.change_screen)

    def change_screen(self):
        try:
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

            self.widget.change_bt.clicked.connect(self.toggle_camera)
            self.camera_popped = True
            self.toggle_camera()

            self.widget.camera_open_bt = QPushButton(locale.get("close_camera", "str_close_camera"))
            self.widget.bt_lt.insertWidget(1, self.widget.camera_open_bt)
            self.widget.camera_open_bt.clicked.connect(self.toggle_open)

            focus_backend = FocusBackend(self.daq_selector.daq())
            self.widget.main_lt.removeWidget(self.daq_selector)
            self.daq_selector.close()
            self.focus_frontend = FocusFrontend(backend=focus_backend)
            self.focus_frontend.show()
            self.tab_frontend = TabsFrontend(self.image_ft.image, lockin, motor_interface, focus_backend)
            self.point_gen_ft = self.tab_frontend.point_gen_ft
            self.widget.main_lt.addWidget(self.tab_frontend)
        except:
            traceback.print_exc()
            sys.exit()

    def closeEvent(self, event):
        self.is_closing = True
        if self.image_ft is not None:
            self.image_ft.close()
        event.accept()

    def toggle_camera(self):
        if self.camera_open:
            if self.camera_popped:
                self.widget.over_main_lt.addWidget(self.image_ft)
                self.image_ft.closed_target = None

                self.widget.change_bt.setText(locale.get("pop_out_camera", "str_pop_out_camera"))
                self.camera_popped = False
            else:
                self.widget.over_main_lt.removeWidget(self.image_ft)
                new_image = CameraOnlyWindow(backend=self.camera_bc)
                self.image_ft.image.new_image_data(new_image.image)
                self.point_gen_ft.connect_image(new_image.image)
                self.image_ft.deleteLater()
                self.image_ft = new_image
                self.image_ft.show()

                self.image_ft.closed_target = self
                self.widget.change_bt.setText(locale.get("pop_in_camera", "str_pop_in_camera"))
                self.camera_popped = True

    def toggle_open(self):
        self.image_ft.toggle_take_photos()
        if self.camera_open:
            self.widget.camera_open_bt.setText(locale.get("open_camera", "str_open_camera"))
            if self.camera_popped:
                self.image_ft.hide()
            else:
                self.widget.over_main_lt.removeWidget(self.image_ft)
                self.image_ft.hide()

            self.camera_open = False

        else:
            self.widget.camera_open_bt.setText(locale.get("close_camera", "str_close_camera"))
            if self.camera_popped:
                self.image_ft.show()
            else:
                self.widget.over_main_lt.addWidget(self.image_ft)
                self.image_ft.show()

            self.camera_open = True
