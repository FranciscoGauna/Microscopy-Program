from PyQt5.QtWidgets import QComboBox
from lantz.qt import Frontend
from PyQt5.QtCore import QTimer
from Backend.lockin_options_backend import LockinControl
from View.localization import locale


class LockinOptions(Frontend):
    backend: LockinControl
    gui = ('UI', 'lockin_options.ui')

    def setupUi(self):
        self.widget.roll_off_label.setText(locale.get("roll_off", "str_roll_off"))
        self.widget.roll_off_cb.addItem("6 dB/oct")
        self.widget.roll_off_cb.addItem("12 dB/oct")
        self.widget.roll_off_cb.addItem("24 dB/oct")

        self.widget.tc_label.setText(locale.get("time_constant", "str_time_constant"))
        self.widget.tc_cb.addItem("0.25 ms")
        self.widget.tc_cb.addItem("0.5 ms")
        self.widget.tc_cb.addItem("1 ms")
        self.widget.tc_cb.addItem("2 ms")
        self.widget.tc_cb.addItem("5 ms")
        self.widget.tc_cb.addItem("10 ms")
        self.widget.tc_cb.addItem("20 ms")
        self.widget.tc_cb.addItem("50 ms")
        self.widget.tc_cb.addItem("0.1 s")
        self.widget.tc_cb.addItem("0.2 s")
        self.widget.tc_cb.addItem("0.5 s")
        self.widget.tc_cb.addItem("2 s")
        self.widget.tc_cb.addItem("1 s")
        self.widget.tc_cb.addItem("5 s")

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

    def set_roll_off(self):
        self.backend.set_lockin_rf(self.widget.roll_off_cb.currentIndex())
