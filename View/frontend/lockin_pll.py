from lantz.qt import Frontend
from PyQt5.QtCore import QTimer
from lantz.qt.connect import connect_feat

from Backend.lockin_options import LockinBackend
from View.localization import locale


class LockinPll(Frontend):
    backend: LockinBackend
    gui = ('UI', 'lockin_pll.ui')
    timer = QTimer()

    def setupUi(self):
        super().setupUi()

        self.widget.pll_check.setText(locale.get("external_reference", "str_external_reference"))

        self.widget.ext_f_label.setText(locale.get("reference_frequency", "str_reference_frequency"))

        self.widget.frec_label.setText(locale.get("lockin_frequency", "str_lockin_frequency"))
        self.widget.amp_label.setText(locale.get("lockin_amplitude", "str_lockin_amplitude"))
        self.widget.phase_label.setText(locale.get("lockin_phase", "str_lockin_phase"))

        self.widget.overload_label.setText("")

    def connect_backend(self):
        super().connect_backend()
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
