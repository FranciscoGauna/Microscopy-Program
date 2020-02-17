from lantz.qt import Frontend, wrap_driver_cls

from Model.AnfatecDriver import VirtualLockin, AnfatecAMU24
from View.localization import locale


class LockinSelector(Frontend):
    gui = ('UI', 'select_lockin.ui')
    lockins_available = {
        "Virtual": VirtualLockin,
        "AnfatecAMU24": AnfatecAMU24,
    }

    def setupUi(self):
        self.widget.lockin_lb.setText(locale.get("lockin_models", "str_lockin_models"))

        for driver in self.lockins_available:
            self.widget.lockin_cb.addItem(driver)

    def open_lockin(self):
        lockin_name = self.widget.lockin_cb.currentText()
        return wrap_driver_cls(self.lockins_available[lockin_name])()
