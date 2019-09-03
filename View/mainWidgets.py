from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QButtonGroup, QRadioButton, QComboBox
from View.localization import locale


def make_gain_buttons(MainWindow):
    parent_layout = QVBoxLayout()
    parent_layout.addWidget(QLabel(locale.get("box_gain", "str_box_gain")))
    layout = QVBoxLayout()
    widget = QWidget()  # central widget
    widget.setLayout(layout)

    number_group = QButtonGroup(widget)  # Number group
    r0 = QRadioButton(locale.get("high_reserve", "str_high_reserve"))
    r0.pressed.connect(MainWindow.helper.set_high_gain)
    r0.setChecked(True)
    number_group.addButton(r0)
    r1 = QRadioButton(locale.get("normal", "str_normal"))
    r1.pressed.connect(MainWindow.helper.set_medium_gain)
    number_group.addButton(r1)
    r2 = QRadioButton(locale.get("low_noise", "str_low_noise"))
    r2.pressed.connect(MainWindow.helper.set_low_gain)
    number_group.addButton(r2)
    layout.addWidget(r0)
    layout.addWidget(r1)
    layout.addWidget(r2)
    parent_layout.addWidget(widget)
    return parent_layout


def make_time_constant_box(MainWindow):
    parent_layout = QVBoxLayout()
    parent_layout.addWidget(QLabel(locale.get("time_constant", "str_time_constant")))
    parent_layout.addWidget(QComboBox())
    return parent_layout


class Helper():
    def __init__(self, lockin):
        self.lockin = lockin

    def set_high_gain(self):
        self.lockin.set_input_gain(1)

    def set_medium_gain(self):
        self.lockin.set_input_gain(10)

    def set_low_gain(self):
        self.lockin.set_input_gain(100)