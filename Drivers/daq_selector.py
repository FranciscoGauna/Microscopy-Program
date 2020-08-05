from PyQt5.QtCore import Qt

from Drivers.DAQ.daq_driver import VirtualDAQ, ComDAQ

from lantz.qt import Frontend
from View.localization import locale
from config import config_file


class DaqSelector(Frontend):
    gui = ("DAQ", "daq_selector.ui")

    def setupUi(self):
        self.widget.daq_cb.setText(locale.get("virtual_daq", "str_virtual_daq"))
        if config_file["PREVIOUS INSTRUMENTS"]["daq"] == "Virtual":
            self.widget.daq_cb.setCheckState(Qt.Checked)
        else:
            self.widget.daq_cb.setCheckState(Qt.Unchecked)

    def daq(self) -> ComDAQ:
        if self.widget.daq_cb.isChecked():
            config_file["PREVIOUS INSTRUMENTS"]["daq"] = "Virtual"
        else:
            config_file["PREVIOUS INSTRUMENTS"]["daq"] = "Real"
        return ComDAQ() if not self.widget.daq_cb.isChecked() else VirtualDAQ()
