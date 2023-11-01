from SER.interfaces import Component
from lantz.qt import wrap_driver_cls

from .instrument_ui import Lockin, LockinUI
from .anfatec_driver import AnfatecAMU24


class AnfatecLockin(Component):
    def __init__(self):
        self.instrument = Lockin(lockin=wrap_driver_cls(AnfatecAMU24)())
        self.conf_ui = LockinUI(backend=self.instrument)
