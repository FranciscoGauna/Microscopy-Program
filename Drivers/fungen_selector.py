import inspect
import os
from configparser import ConfigParser
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog
from lantz.qt import Frontend
from lantz.drivers.rigol.dg1022 import DG1022

from Drivers.FunGen.sdg5122_driver import SDG5122
from Drivers.FunGen.virtual_fungen import VirtualFungen
from View.localization import locale
from config import config_file


class FungenSelector(Frontend):
    gui = ('Fungen', 'fungen_selector.ui')

    def dg1022(self):
        # driver = DG1022("dummy") Cambiar al posta cuando vamos a pc
        driver = DG1022("dummy")
        driver.initialize()
        return driver

    def sdg5122(self):
        driver = SDG5122("dummy")
        driver.initialize()
        return driver

    def virtual(self):
        driver = VirtualFungen()
        driver.initialize()
        return driver

    fungen_available = {
        "Virtual": virtual,
        "Siglent SDG5122": sdg5122,
        "Rigol DG1022": dg1022,
    }

    def setupUi(self):
        self.widget.fungen_lb.setText(locale.get("fungen_models", "str_fungen_models"))
        self.widget.load_conf_bt.setText(locale.get("load_conf", "str_load_conf"))
        self.widget.load_conf_bt.clicked.connect(self.load_conf)

        for driver in self.fungen_available:
            self.widget.fungen_cb.addItem(driver)

        try:
            self.widget.fungen_cb.setCurrentText(config_file["PREVIOUS INSTRUMENTS"]["fungen"])
        except:
            self.widget.fungen_cb.setCurrentText("Virtual")

    def load_conf(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        folder = os.path.dirname(inspect.getfile(self.__class__))
        file_dialog.setDirectory(os.path.join(folder, "Fungen"))
        file_name, _ = file_dialog.getOpenFileName(self, "Open File", "",
                                                   "Configuration File (*.cfg);;All Files (*)", options=options)
        if file_name:
            self.widget.load_conf_bt.setText(Path(file_name).name)
            self.conf = ConfigParser()
            self.conf.read(file_name)

    def fungen(self):
        return self.fungen_available[self.widget.fungen_cb.currentText()](self)
