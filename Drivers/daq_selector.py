import inspect
import os
from configparser import ConfigParser
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog

from lantz.qt import Frontend

from Drivers.DAQ.daq_driver import ComDaqBackend
from Drivers.DAQ.mc_usb_2527_driver import USB2527DaqBackend
from Drivers.DAQ.virtual_backend import VirtualDaqBackend
from View.localization import locale
from config import config_file


class DaqSelector(Frontend):
    gui = ("DAQ", "daq_selector.ui")
    conf = ConfigParser()

    def usb_2527(self):
        driver = USB2527DaqBackend(self.conf["CONNECTION"]["board_number"])
        return driver

    def comdaq(self):
        driver = ComDaqBackend()
        return driver

    def virtual(self):
        driver = VirtualDaqBackend()
        return driver

    daq_available = {
        "Virtual": virtual,
        "MCC USB2527": usb_2527,
        "MCC ": comdaq,
    }

    def setupUi(self):
        self.widget.daq_lb.setText(locale.get("virtual_daq", "str_virtual_daq"))
        self.widget.load_conf_bt.setText(locale.get("load_conf", "str_load_conf"))
        self.widget.load_conf_bt.clicked.connect(self.load_conf)

        for driver in self.daq_available:
            self.widget.daq_cb.addItem(driver)

        self.widget.daq_cb.setCurrentText(config_file["PREVIOUS INSTRUMENTS"]["lockin"])

    def load_conf(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        folder = os.path.dirname(inspect.getfile(self.__class__))
        file_dialog.setDirectory(os.path.join(folder, "DAQ"))
        file_name, _ = file_dialog.getOpenFileName(self, "Open File", "",
                                                   "Configuration File (*.cfg);;All Files (*)", options=options)
        if file_name:
            self.widget.load_conf_bt.setText(Path(file_name).name)
            self.conf.read(file_name)

    def daq(self) -> VirtualDaqBackend:
        config_file.set("PREVIOUS INSTRUMENTS", "daq", self.widget.daq_cb.currentText())
        return self.daq_available[self.widget.daq_cb.currentText()](self)
