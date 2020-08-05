from lantz.drivers.stanford import SR830
from lantz.qt import Frontend, wrap_driver_cls

from Drivers.Lockin.anfatec_driver import VirtualLockin, AnfatecAMU24
from View.localization import locale
from config import config_file


def Virtual():
    return wrap_driver_cls(VirtualLockin)()

class LockinSelector(Frontend):
    gui = ('Lockin', 'lockin_selector.ui')

    def Anfatec(self):
        return AnfatecAMU24

    def SR830_GPIB(self):
        config_file
        return

    lockins_available = {
        "Virtual": Virtual,
        "AnfatecAMU24": AnfatecAMU24,
        "SR830 GPIB": SR830_GPIB,
        "SR830 ": SR830.via_gpib,
        "SR844": SR830,
    }

    def setupUi(self):
        self.widget.lockin_lb.setText(locale.get("lockin_models", "str_lockin_models"))

        for driver in self.lockins_available:
            self.widget.lockin_cb.addItem(driver)

        self.widget.lockin_cb.setCurrentText(config_file["PREVIOUS INSTRUMENTS"]["lockin"])

    def lockin(self):
        config_file.set("PREVIOUS INSTRUMENTS", "lockin", self.widget.lockin_cb.currentText())

        return self.lockins_available[self.widget.lockin_cb.currentText()]()

