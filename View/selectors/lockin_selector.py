import inspect
import os
from configparser import ConfigParser
from pathlib import Path

import visa
from PyQt5.QtWidgets import QFileDialog
from lantz.drivers.stanford import SR830
from lantz.qt import Frontend, wrap_driver_cls
from lantz.core import messagebased

from Drivers.Lockin.LI5655 import LI5655, ResourceDummy
from Drivers.Lockin.anfatec_driver import VirtualLockin, AnfatecAMU24
from View.localization import locale
from config import config_file


class LockinSelector(Frontend):
    gui = ('ui', 'lockin_selector.ui')
    conf: ConfigParser

    def Virtual(self):
        return wrap_driver_cls(VirtualLockin)()

    def Anfatec(self):
        driver = wrap_driver_cls(AnfatecAMU24)()
        return driver

    def SR830_GPIB(self):
        try:
            driver = SR830("dummy")
            # driver = wrap_driver_cls(SR830).via_gpib(self.conf["CONNECTION"]["gpib_address"])
            driver.initialize()
            driver.resource = ResourceDummy()
            driver.send = driver.query
            driver.amplitude = driver.analog_value['r']
            driver.phase = driver.analog_value['t']
            driver.real_part_x = driver.analog_value['x']
            driver.imaginary_part_y = driver.analog_value['y']
            return driver
        except AttributeError:
            raise Exception(locale.get("config_missing", "str_config_missing"))

    def LI5655_USB(self):
        """
        This method redefines the resource manager for the Lantz library, because the instance of visa manager doesn't
        pick up the presence of this driver
        :return: LI5655 driver class instanced and initialized
        """
        try:
            messagebased._resource_manager = visa.ResourceManager() # If this code is missing
            driver = wrap_driver_cls(LI5655).via_usb()
            driver.initialize()
            return driver
        except AttributeError:
            raise Exception(locale.get("config_missing", "str_config_missing"))

    lockins_available = {
        "Virtual": Virtual,
        "AnfatecAMU24": AnfatecAMU24,
        "SR830 GPIB": SR830_GPIB,
        "SR844 GPIB": SR830_GPIB,
        "LI5655": LI5655_USB,
    }

    def setupUi(self):
        self.widget.lockin_lb.setText(locale.get("lockin_models", "str_lockin_models"))
        self.widget.load_conf_bt.setText(locale.get("load_conf", "str_load_conf"))
        self.widget.load_conf_bt.clicked.connect(self.load_conf)

        for driver in self.lockins_available:
            self.widget.lockin_cb.addItem(driver)

        self.widget.lockin_cb.setCurrentText(config_file["PREVIOUS INSTRUMENTS"]["lockin"])

    def load_conf(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        folder = os.path.dirname(inspect.getfile(self.__class__))
        file_dialog.setDirectory(os.path.join(folder, "Lockin"))
        file_name, _ = file_dialog.getOpenFileName(self, "Open File", "",
                                                   "Configuration File (*.cfg);;All Files (*)", options=options)
        if file_name:
            self.widget.load_conf_bt.setText(Path(file_name).name)
            self.conf = ConfigParser()
            self.conf.read(file_name)

    def lockin(self):
        config_file.set("PREVIOUS INSTRUMENTS", "lockin", self.widget.lockin_cb.currentText())
        return self.lockins_available[self.widget.lockin_cb.currentText()](self)
