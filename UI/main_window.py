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
from components.Lockin import AnfatecLockin
from components.Platina import PlatinaComponent
from components.Platina.motor import get_available_motors, Motor


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

    camera_ops: dict[str, Callable[[], VideoCapture]]
    virtual_camera_cb: QCheckBox

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

        self.show()

    def load_options(self):
        self.fungen_ops = {
            "Virtual": HPFunGen.virtual,
            "HP 33120A": lambda: HPFunGen.via_prologix_gpib(10)
        }
        self.fungen_cb.addItems(self.fungen_ops.keys())

        self.lockin_ops = {
            "Virtual": AnfatecLockin.virtual,
            "Anfatec": AnfatecLockin.real
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
            "Lucam": LucamCam  # TODO: change this to the proper camera
        }
        self.camera_cb.addItems(self.camera_ops.keys())

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
        print("switch_window")
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

        ser_widget = get_main_widget([fungen_component, platina_component],
                                     [lockin_component],
                                     [], [],
                                     coupling_ui_options={"enabled": True, "x": 1, "y": 0})

        self.experiment_layout.addWidget(ser_widget, 0, 0)
        self.stack_widget.setCurrentWidget(self.experiment_page)

    def close_components(self):
        if self.platina_comp is not None:
            self.platina_comp.close_component()
