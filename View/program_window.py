import sys
import traceback
from PyQt5.QtWidgets import QPushButton, QMessageBox
from lantz.qt import Frontend

from Backend.camera_backend import CameraBackend
from Backend.focus_backend import FocusBackend
from Backend.platina_backend import PlatinaBackend
from View.frontend.camera_control_ui import ImageDrawerFt
from View.frontend.camera_only import CameraOnlyWindow
from View.frontend.focus_frontend import FocusFrontend
from View.frontend.motor_frontend import DualMotorFrontend
from Drivers.motor_selector import MotorAlreadyOpenException
from View.localization import locale
from View.selector_window import SelectorWindow
from View.tabs_window import TabsFrontend
from config import config_file


class ProgramWindow(Frontend):
    backend: PlatinaBackend
    gui = ("frontend", "UI", "main.ui")
    initialized = False
    is_closing = False
    image_ft = None
    camera_popped = False
    camera_open = True

    # First Window
    selector_frontend: SelectorWindow

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

        self.selector_frontend = SelectorWindow()
        self.widget.main_lt.addWidget(self.selector_frontend)
        self.widget.change_bt.clicked.connect(self.change_screen)

    def change_screen(self):
        try:
            if self.initialized:
                return

            self.initialized = True

            try:
                motor_backend = self.selector_frontend.dual_motor_backend()
                lockin = self.selector_frontend.lockin()
                daq = self.selector_frontend.daq()
                camera = self.selector_frontend.camera()
                fungen = self.selector_frontend.fungen()
            except Exception as e:
                error_dialog = QMessageBox()
                error_dialog.setText(str(e))
                error_dialog.exec()
                self.initialized = False
                return

            self.camera_bc = CameraBackend(camera)
            self.image_ft = CameraOnlyWindow(backend=self.camera_bc)

            focus_backend = FocusBackend(daq)

            self.tab_frontend = TabsFrontend(self.image_ft.image, lockin, motor_backend, focus_backend, fungen)
            self.point_gen_ft = self.tab_frontend.point_gen_ft
            self.widget.main_lt.addWidget(self.tab_frontend)

            # Remove selectors
            self.widget.main_lt.removeWidget(self.selector_frontend)
            self.selector_frontend.close()

            # Create window for focus control
            self.focus_frontend = FocusFrontend(self, backend=focus_backend)
            self.focus_frontend.show()

            # Setup buttons for camera control
            self.widget.change_bt.clicked.connect(self.toggle_camera)
            self.camera_popped = True
            self.toggle_camera()
            self.widget.camera_open_bt = QPushButton(locale.get("close_camera", "str_close_camera"))
            self.widget.bt_lt.insertWidget(1, self.widget.camera_open_bt)
            self.widget.camera_open_bt.clicked.connect(self.toggle_open)

        except:
            traceback.print_exc()
            sys.exit()

    def closeEvent(self, event):
        with open('config.ini', 'w+') as configfile:
            config_file.write(configfile)

        self.is_closing = True
        if self.image_ft is not None:
            self.image_ft.close()
        if hasattr(self, "focus_frontend"):
            self.focus_frontend.close()
        self.deleteLater()
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
