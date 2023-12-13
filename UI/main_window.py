from os import path
from typing import Callable

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QStackedWidget, QComboBox, QLabel
from SER import get_main_widget
from SER.interfaces import ComponentInitialization, Component
from lantz.qt import wrap_driver_cls

from components.HP33120AFunGen import HPFunGen
from components.Lockin import AnfatecLockin
from components.Platina import PlatinaComponent
from components.Platina.instrument_ui import Platina
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
    motor_ops: dict[str, str]

    def __init__(self):
        super().__init__()
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "main_window.ui")
        uic.loadUi(ui_file_path, self)
        self.setWindowTitle("Microscopy-Program")

        self.experiment_layout = self.experiment_page.layout()
        self.launch_button.pressed.connect(self.switch_window)

        self.load_options()

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

    def switch_window(self):
        fungen_comp = self.fungen_ops[self.fungen_cb.currentText()]()
        fungen_component = ComponentInitialization(fungen_comp, -9000, 0, 1, "Fungen 1")
        lockin_comp = self.lockin_ops[self.lockin_cb.currentText()]()
        lockin_component = ComponentInitialization(lockin_comp, -9000, 1, 1, "Lockin")

        x_motor = wrap_driver_cls(Motor)()
        x_motor.open_motor(self.motor_ops[self.motor_x_cb.currentText()])
        x_motor_comp = PlatinaComponent(motor=x_motor)
        x_motor_component = ComponentInitialization(x_motor_comp, 0, 0, 0, "Motor 1")

        ser_widget = get_main_widget([fungen_component, x_motor_component],
                                     [lockin_component],
                                     [], [])

        self.experiment_layout.addWidget(ser_widget, 0, 0)
        self.stack_widget.setCurrentWidget(self.experiment_page)
