from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QButtonGroup, QRadioButton, QComboBox
from View.localization import locale
from Model.AnfatecDriver import Coupling


class OptionsPanel:
    def __init__(self, lockin):
        self.lockin = lockin
        self.time_constant_box = None
        self.roll_off_box = None
        self.harmonics_box = None

    def make_layout(self):
        layout = QVBoxLayout()
        upper_layout = QVBoxLayout()
        under_layout = QVBoxLayout()
        upper_layout.addStretch(0)

        upper_layout.addLayout(self.make_roll_off_box())
        upper_layout.addLayout(self.make_time_constant_box())
        upper_layout.addLayout(self.make_harmonics_box())
        under_layout.addLayout(self.make_gain_buttons())
        under_layout.addLayout(self.make_coupling_buttons())

        under_layout.addStretch(1)
        layout.addLayout(upper_layout)
        layout.addLayout(under_layout)
        return layout

    def make_roll_off_box(self):
        parent_layout = QVBoxLayout()
        parent_layout.addWidget(QLabel(locale.get("roll_off", "str_roll_off")))
        roll_off_box = QComboBox()
        roll_off_box.addItem("6 dB/oct")
        roll_off_box.addItem("12 dB/oct")
        roll_off_box.addItem("24 dB/oct")
        roll_off_box.setCurrentIndex(self.lockin.get_lockin_roll_off())
        roll_off_box.currentIndexChanged.connect(self.set_roll_off)
        parent_layout.addWidget(roll_off_box)
        self.roll_off_box = roll_off_box
        return parent_layout

    def set_roll_off(self):
        self.lockin.set_lockin_roll_off(self.roll_off_box.currentIndex())

    def make_time_constant_box(self):
        parent_layout = QVBoxLayout()
        parent_layout.addWidget(QLabel(locale.get("time_constant", "str_time_constant")))
        time_constant_box = QComboBox()
        time_constant_box.addItem("0.25 ms")
        time_constant_box.addItem("0.5 ms")
        time_constant_box.addItem("1 ms")
        time_constant_box.addItem("2 ms")
        time_constant_box.addItem("5 ms")
        time_constant_box.addItem("10 ms")
        time_constant_box.addItem("20 ms")
        time_constant_box.addItem("50 ms")
        time_constant_box.addItem("0.1 s")
        time_constant_box.addItem("0.2 s")
        time_constant_box.addItem("0.5 s")
        time_constant_box.addItem("1 s")
        time_constant_box.addItem("2 s")
        time_constant_box.addItem("5 s")
        time_constant_box.setCurrentIndex(self.lockin.get_lockin_time_constant())
        time_constant_box.currentIndexChanged.connect(self.change_time_constant)
        parent_layout.addWidget(time_constant_box)
        self.time_constant_box = time_constant_box
        return parent_layout

    def change_time_constant(self):
        # Este codigo usa el index y la variable times para convertir a en b
        times = [20, 20, 20, 20, 20, 20, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        self.lockin.set_lockin_time_constant(self.time_constant_box.currentIndex())

    def make_harmonics_box(self):
        parent_layout = QVBoxLayout()
        parent_layout.addWidget(QLabel(locale.get("harmonics", "str_harmonics")))
        harmonics_box = QComboBox()
        harmonics_box.addItem("1")
        harmonics_box.addItem("2")
        harmonics_box.addItem("3")
        harmonics_box.addItem("4")
        harmonics_box.addItem("5")
        harmonics_box.addItem("6")
        harmonics_box.addItem("7")
        harmonics_box.addItem("8")
        harmonics_box.addItem("9")
        harmonics_box.addItem("10")
        harmonics_box.addItem("11")
        harmonics_box.addItem("12")
        harmonics_box.addItem("13")
        harmonics_box.addItem("14")
        harmonics_box.addItem("15")
        harmonics_box.setCurrentIndex(self.lockin.harmonic - 1)
        harmonics_box.currentIndexChanged.connect(self.change_harmonic)
        parent_layout.addWidget(harmonics_box)
        self.harmonics_box = harmonics_box
        return parent_layout

    def change_harmonic(self):
        self.lockin.harmonic = self.harmonics_box.currentIndex() + 1

    def make_gain_buttons(self):
        parent_layout = QVBoxLayout()
        parent_layout.addWidget(QLabel(locale.get("box_gain", "str_box_gain")))
        layout = QVBoxLayout()
        widget = QWidget()  # central widget
        widget.setLayout(layout)

        number_group = QButtonGroup(widget)  # Number group
        r0 = QRadioButton(locale.get("high_reserve", "str_high_reserve"))
        r0.pressed.connect(self.set_high_gain)
        number_group.addButton(r0)
        r1 = QRadioButton(locale.get("normal", "str_normal"))
        r1.pressed.connect(self.set_medium_gain)
        number_group.addButton(r1)
        r2 = QRadioButton(locale.get("low_noise", "str_low_noise"))
        r2.pressed.connect(self.set_low_gain)
        if self.lockin.input_gain == 1:
            r0.setChecked(True)
        elif self.lockin.input_gain == 10:
            r1.setChecked(True)
        else:
            r2.setChecked(True)
        number_group.addButton(r2)
        layout.addWidget(r0)
        layout.addWidget(r1)
        layout.addWidget(r2)
        parent_layout.addWidget(widget)
        return parent_layout

    def set_high_gain(self):
        self.lockin.input_gain = 1

    def set_medium_gain(self):
        self.lockin.input_gain = 10

    def set_low_gain(self):
        self.lockin.input_gain = 100

    def make_coupling_buttons(self):
        parent_layout = QVBoxLayout()
        parent_layout.addWidget(QLabel(locale.get("box_coupling", "str_box_coupling")))
        layout = QVBoxLayout()
        widget = QWidget()  # central widget
        widget.setLayout(layout)

        number_group = QButtonGroup(widget)  # Number group
        r0 = QRadioButton(locale.get("ac_coupling", "str_ac_coupling"))
        r0.pressed.connect(self.set_ac_coupling)
        number_group.addButton(r0)
        r1 = QRadioButton(locale.get("dc_coupling", "str_dc_coupling"))
        r1.pressed.connect(self.set_dc_coupling)
        number_group.addButton(r1)
        if self.lockin.coupling == Coupling.ac:
            r0.setChecked(True)
        else:
            r1.setChecked(True)
        layout.addWidget(r0)
        layout.addWidget(r1)
        parent_layout.addWidget(widget)
        return parent_layout

    def set_ac_coupling(self):
        self.lockin.coupling = Coupling.ac

    def set_dc_coupling(self):
        self.lockin.coupling = Coupling.dc
