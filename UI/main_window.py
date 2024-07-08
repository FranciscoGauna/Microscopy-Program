from os import path
from typing import Callable

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QStackedWidget, QComboBox, QLabel, \
    QFileDialog, QCheckBox
from SER import get_main_widget
from SER.interfaces import ComponentInitialization, Component
from cv2 import VideoCapture
from lantz.qt import wrap_driver_cls

from components.CameraPlatina import CameraPlatinaComponent, CameraBackend, VirtualCamera
from components.CameraPlatina.camera import LucamCam
from components.HP33120AFunGen import HPFunGen
from components.LinePlotter import LinePlotter
from components.Lockin import AnfatecLockin
from components.Oven import LinkamOven
from components.Platina import PlatinaComponent
from components.Platina.motor import get_available_motors, Motor
from components.USBDAQ import USB2527DAC


class MainWindow(QMainWindow):
    stack_widget: QStackedWidget

    experiment_page: QWidget
    experiment_layout: QGridLayout

    launch_button: QPushButton

    fungen_label: QLabel
    fungen_cb: QComboBox
    fungen_ops: dict[str, Callable[[], Component]]
    lockin_label: QLabel
    lockin_cb: QComboBox
    lockin_ops: dict[str, Callable[[], Component]]
    motor_x_label: QLabel
    motor_x_cb: QComboBox
    motor_x_bt: QPushButton
    motor_y_label: QLabel
    motor_y_cb: QComboBox
    motor_y_bt: QPushButton
    motor_ops: dict[str, str]

    camera_cb: QComboBox
    camera_ops: dict[str, Callable[[], VideoCapture]]

    oven_cb: QComboBox
    oven_ops: dict[str, Callable[[], Component]]

    dac_cb: QComboBox
    dac_ops: dict[str, Callable[[], Component]]

    def __init__(self):
        super().__init__()
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "main_window.ui")
        uic.loadUi(ui_file_path, self)
        self.setWindowTitle("Microscopy-Program")

        self.experiment_layout = self.experiment_page.layout()
        self.launch_button.pressed.connect(self.switch_window)

        self.load_options()
        self.motor_x_filename = None
        self.motor_y_filename = None

        # Components. We store them if it's necessary to close them specifically if finished before execution
        self.fungen_comp = None
        self.lockin_comp = None
        self.platina_comp = None
        self.oven_comp = None
        self.dac_comp = None

        self.show()

    def load_options(self):
        self.fungen_ops = {
            "Virtual": HPFunGen.virtual,
            "HP 33120A": lambda: HPFunGen.via_prologix_gpib(10),
            "Rigol": HPFunGen.rigol
        }
        self.fungen_cb.addItems(self.fungen_ops.keys())

        self.lockin_ops = {
            "Virtual": AnfatecLockin.virtual,
            "Anfatec": AnfatecLockin.real,
            "LI5655": AnfatecLockin.LI5655
        }
        self.lockin_cb.addItems(self.lockin_ops.keys())

        self.motor_ops = get_available_motors()
        self.motor_ops["Virtual"] = "virtual"
        self.motor_x_cb.addItems(self.motor_ops.keys())
        self.motor_y_cb.addItems(self.motor_ops.keys())
        self.motor_x_bt.pressed.connect(lambda: self.load_motor_configuration("x"))
        self.motor_y_bt.pressed.connect(lambda: self.load_motor_configuration("y"))

        self.camera_ops = {
            "Virtual": VirtualCamera,
            "Web Cam": lambda: VideoCapture(0),
            "Lucam": LucamCam
        }
        self.camera_cb.addItems(self.camera_ops.keys())

        self.oven_ops = {
            "Virtual": LinkamOven.virtual,
            "Linkam TMS 94": lambda: LinkamOven.real(15),
        }
        self.oven_cb.addItems(self.oven_ops.keys())

        self.dac_ops = {
            "Virtual": USB2527DAC.virtual,
            "USB2527": lambda: USB2527DAC.real(0),
        }
        self.dac_cb.addItems(self.dac_ops.keys())

    def load_motor_configuration(self, target):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory("components/Platina")  # TODO: see if we need to change this
        file_name, _ = file_dialog.getOpenFileName(self, "Open File", "",
                                                   "Config File (*.cfg);;All Files (*)", options=options)

        if file_name:
            if target == "x":  # TODO: see if this is too ugly, maybe change to a generic attribute
                self.motor_x_filename = file_name
            else:
                self.motor_y_filename = file_name

    def switch_window(self):
        self.fungen_comp = self.fungen_ops[self.fungen_cb.currentText()]()
        fungen_component = ComponentInitialization(self.fungen_comp, 0, 0, 1, "Fungen 1")
        self.lockin_comp = self.lockin_ops[self.lockin_cb.currentText()]()
        lockin_component = ComponentInitialization(self.lockin_comp, -9000, 1, 1, "Lockin")

        # TODO: grab the keys for moving the motor from a config
        x_motor = wrap_driver_cls(Motor)()
        x_motor.open_motor(self.motor_ops[self.motor_x_cb.currentText()])
        x_motor_comp = PlatinaComponent(motor=x_motor, filename=self.motor_x_filename)
        y_motor = wrap_driver_cls(Motor)()
        y_motor.open_motor(self.motor_ops[self.motor_y_cb.currentText()])
        y_motor_comp = PlatinaComponent(y_motor, self.motor_y_filename, "down", "up")

        camera = self.camera_ops[self.camera_cb.currentText()]()
        camera_back = CameraBackend(camera)
        self.platina_comp = CameraPlatinaComponent(x_motor_comp, y_motor_comp, camera_back)

        platina_component = ComponentInitialization(self.platina_comp, 1, 0, 0, "Platina")

        self.oven_comp = self.oven_ops[self.oven_cb.currentText()]()
        oven_component = ComponentInitialization(self.oven_comp, -10, 0, 2, "Oven")

        self.dac_comp = self.dac_ops[self.dac_cb.currentText()]()
        dac_component = ComponentInitialization(self.dac_comp, -10, 1, 0, "DAC")

        self.amplitude_graph = LinePlotter(("Fungen 1", "frequency", "Freq"),
                                           ("Lockin", "amplitude", "Amplitude"), scatter=True, x=0)
        self.phase_graph = LinePlotter(("Fungen 1", "frequency", "Freq"),
                                       ("Lockin", "phase", "Phase"), scatter=True, x=1)

        ser_widget = get_main_widget([fungen_component, platina_component, oven_component],
                                     [lockin_component, dac_component],
                                     [self.platina_comp.run_ui, self.amplitude_graph, self.phase_graph], [],
                                     coupling_ui_options={"enabled": True, "x": 1, "y": 2})

        self.experiment_layout.addWidget(ser_widget, 0, 0)
        self.stack_widget.setCurrentWidget(self.experiment_page)

    def close_components(self):
        if self.platina_comp is not None:
            self.platina_comp.close_component()
        if self.dac_comp is not None:
            self.dac_comp.close_component()
        if self.lockin_comp is not None:
            self.lockin_comp.close_component()
