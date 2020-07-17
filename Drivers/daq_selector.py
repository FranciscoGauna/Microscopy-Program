from Drivers.DAQ.daq_driver import VirtualDAQ, ComDAQ

from lantz.qt import Frontend
from View.localization import locale


class DaqSelectorFrontend(Frontend):
    gui = ("DAQ", "daq_selector.ui")

    def setupUi(self):
        self.widget.daq_rb.setText(locale.get("virtual_daq", "str_virtual_daq"))

    def daq(self) -> ComDAQ:
        return ComDAQ() if not self.widget.daq_rb.isChecked() else VirtualDAQ()
