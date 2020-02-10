from PyQt5.QtWidgets import QComboBox
from lantz.qt import Frontend
from PyQt5.QtCore import QTimer
from lantz.qt.connect import connect_feat

from Backend.lockin_options import LockinControl
from View.localization import locale
from Model.AnfatecDriver import Coupling


class LockinOptions(Frontend):
    backend: LockinControl
    gui = ('UI', 'lockin_options.ui')

    def setupUi(self):
        self.widget.roll_off_label.setText(locale.get("roll_off", "str_roll_off"))
        self.widget.roll_off_cb.addItem("6 dB/oct")
        self.widget.roll_off_cb.addItem("12 dB/oct")
        self.widget.roll_off_cb.addItem("24 dB/oct")

        self.widget.tc_label.setText(locale.get("time_constant_ms", "str_time_constant_ms"))

        self.widget.h_label.setText(locale.get("harmonic", "str_harmonic"))

        self.widget.ig_label.setText(locale.get("input_gain", "str_input_gain"))
        self.widget.ig_0.setText(locale.get("1_time", "str_1_time"))
        self.widget.ig_1.setText(locale.get("10_times", "str_10_times"))
        self.widget.ig_2.setText(locale.get("100_times", "str_100_times"))

        self.widget.coupling_label.setText(locale.get("coupling", "str_coupling"))
        self.widget.coupling_0.setText(locale.get("dc_coupling", "str_dc_coupling"))
        self.widget.coupling_1.setText(locale.get("ac_coupling", "str_ac_coupling"))

        super().setupUi()

    def connect_backend(self):
        super().connect_backend()

        self.widget.roll_off_cb.setCurrentIndex(self.backend.get_lockin_rf())
        self.widget.roll_off_cb.currentIndexChanged.connect(self.set_roll_off)

        self.widget.tc_cb.setCurrentIndex(self.backend.get_lockin_tc())
        self.widget.roll_off_cb.currentIndexChanged.connect(self.set_tc)

        connect_feat(self.widget.h_spinbox, self.backend.lockin, "harmonic")
        connect_feat(self.widget.tc_cb, self.backend.lockin, "time_constant")

        ig_rb = {1: self.widget.ig_0,
                 10: self.widget.ig_1,
                 100: self.widget.ig_2}
        ig_rb[self.backend.get_input_gain()].setChecked(True)
        self.widget.ig_0.pressed.connect(lambda: self.backend.set_input_gain(1))
        self.widget.ig_1.pressed.connect(lambda: self.backend.set_input_gain(10))
        self.widget.ig_2.pressed.connect(lambda: self.backend.set_input_gain(100))

        coupling_rb = {Coupling.dc: self.widget.coupling_0,
                       Coupling.ac: self.widget.coupling_1}
        coupling_rb[self.backend.get_coupling()].setChecked(True)
        self.widget.coupling_0.pressed.connect(lambda: self.backend.set_coupling(Coupling.dc))
        self.widget.coupling_1.pressed.connect(lambda: self.backend.set_coupling(Coupling.ac))

    def set_roll_off(self):
        self.backend.set_lockin_rf(self.widget.roll_off_cb.currentIndex())

    def set_tc(self):
        self.backend.set_lockin_tc(self.widget.tc_cb.currentIndex())
