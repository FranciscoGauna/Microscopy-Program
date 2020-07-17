from lantz.qt import Frontend
from lantz.qt.connect import connect_feat
from PyQt5.QtCore import QTimer

from Drivers.Lockin.anfatec_driver import Coupling
from Backend.lockin_options import LockinBackend
from View.localization import locale


class LockinTabOptions(Frontend):
    backend: LockinBackend
    gui = ('UI', 'lockin_tab_options.ui')
    timer = QTimer()

    def setupUi(self):
        self.widget.roll_off_label.setText(locale.get("roll_off", "str_roll_off"))
        self.widget.tc_label.setText(locale.get("time_constant", "str_time_constant"))

        self.widget.h_label.setText(locale.get("harmonic", "str_harmonic"))

        self.widget.ig_label.setText(locale.get("input_gain", "str_input_gain"))
        self.widget.ig_0.setText(locale.get("1_time", "str_1_time"))
        self.widget.ig_1.setText(locale.get("10_times", "str_10_times"))
        self.widget.ig_2.setText(locale.get("100_times", "str_100_times"))

        self.widget.coupling_label.setText(locale.get("coupling", "str_coupling"))
        self.widget.coupling_0.setText(locale.get("dc_coupling", "str_dc_coupling"))
        self.widget.coupling_1.setText(locale.get("ac_coupling", "str_ac_coupling"))

        self.widget.pll_check.setText(locale.get("external_reference", "str_external_reference"))

        self.widget.ext_f_label.setText(locale.get("reference_frequency", "str_reference_frequency"))

        self.widget.frec_label.setText(locale.get("lockin_frequency", "str_lockin_frequency"))
        self.widget.amp_label.setText(locale.get("lockin_amplitude", "str_lockin_amplitude"))
        self.widget.phase_label.setText(locale.get("lockin_phase", "str_lockin_phase"))

        self.widget.overload_label.setText("")

        super().setupUi()

    def connect_backend(self):
        super().connect_backend()

        connect_feat(self.widget.h_spinbox, self.backend.lockin, "harmonic")
        connect_feat(self.widget.roll_off_cb, self.backend.lockin, "lockin_roll_off")
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

        self.widget.pll_check.toggled.connect(self.change_panel)
        self.widget.pll_check.setChecked(self.backend.pll())

        connect_feat(self.widget.frec_input, self.backend.lockin, "lockin_frequency")
        connect_feat(self.widget.amp_input, self.backend.lockin, "lockin_amplitude")
        connect_feat(self.widget.phase_input, self.backend.lockin, "lockin_phase")

        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_ext_f)
        self.timer.timeout.connect(self.check_overload)
        self.timer.start()

    def change_panel(self):
        if self.widget.pll_check.isChecked():
            self.widget.pll_spanel.setCurrentWidget(self.widget.on_widget)
        else:
            self.widget.pll_spanel.setCurrentWidget(self.widget.off_widget)
        self.backend.toggle_pll()

    def check_overload(self):
        if self.backend.overload():
            self.widget.overload_label.setText(locale.get("overload", "str_overload"))
            self.widget.overload_label.setStyleSheet("background-color: red;")
        else:
            self.widget.overload_label.setText("")
            self.widget.overload_label.setStyleSheet("")

    def check_ext_f(self):
        self.widget.ext_f_display.setValue(self.backend.ext_frequency())
