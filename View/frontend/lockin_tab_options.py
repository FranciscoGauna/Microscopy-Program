import sys
import traceback

from lantz.qt import Frontend
from lantz.qt.connect import connect_feat
from PyQt5.QtCore import QTimer

from Drivers.Lockin.anfatec_driver import Coupling
from Backend.lockin_backend import LockinBackend
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

        self.widget.coupling_label.setText(locale.get("coupling", "str_coupling"))

        self.widget.pll_check.setText(locale.get("external_reference", "str_external_reference"))

        self.widget.ext_f_label.setText(locale.get("external_frequency", "str_external_frequency"))

        self.widget.frec_label.setText(locale.get("lockin_frequency", "str_lockin_frequency"))
        self.widget.amp_label.setText(locale.get("lockin_amplitude", "str_lockin_amplitude"))
        self.widget.phase_label.setText(locale.get("lockin_phase", "str_lockin_phase"))

        self.widget.overload_label.setText("")

        super().setupUi()

    def connect_backend(self):
        try:
            super().connect_backend()

            connect_feat(self.widget.h_spinbox, self.backend.lockin, "harmonic")
            connect_feat(self.widget.roll_off_cb, self.backend.lockin, "filter_db_per_oct")
            connect_feat(self.widget.tc_cb, self.backend.lockin, "time_constants")
            connect_feat(self.widget.ig_cb, self.backend.lockin, "sensitivity")
            connect_feat(self.widget.coupling_cb, self.backend.lockin, "input_coupling")

            self.widget.pll_check.toggled.connect(self.change_panel)
            self.widget.pll_check.setChecked(self.backend.pll())

            connect_feat(self.widget.frec_input, self.backend.lockin, "frequency")
            connect_feat(self.widget.amp_input, self.backend.lockin, "sine_output_amplitude")
            connect_feat(self.widget.phase_input, self.backend.lockin, "reference_phase_shift")

            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.check_ext_f)
            self.timer.timeout.connect(self.check_overload)
            self.timer.start()
        except:
            traceback.print_exc()

    def change_panel(self):
        try:
            if self.widget.pll_check.isChecked():
                self.widget.pll_spanel.setCurrentWidget(self.widget.on_widget)
            else:
                self.widget.pll_spanel.setCurrentWidget(self.widget.off_widget)
            self.backend.toggle_pll()
        except:
            traceback.print_exc()
            sys.exit()

    def check_overload(self):
        try:
            if self.backend.overload():
                self.widget.overload_label.setText(locale.get("overload", "str_overload"))
                self.widget.overload_label.setStyleSheet("background-color: red;")
            else:
                self.widget.overload_label.setText("")
                self.widget.overload_label.setStyleSheet("")
        except:
            traceback.print_exc()
            sys.exit()

    def check_ext_f(self):
        try:
            self.widget.ext_f_display.setValue(self.backend.ext_frequency())
        except:
            traceback.print_exc()
            sys.exit()
