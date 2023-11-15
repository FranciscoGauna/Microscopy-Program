from SER.interfaces import Component
from lantz.qt import wrap_driver_cls

from .instrument_ui import Lockin, LockinUI
from .anfatec_driver import AnfatecAMU24, VirtualLockin


class AnfatecLockin(Component):
    def __init__(self, lockin):
        self.instrument = Lockin(lockin=lockin)
        self.conf_ui = LockinUI(backend=self.instrument)

    @classmethod
    def virtual(cls):
        return cls(wrap_driver_cls(VirtualLockin)())

    @classmethod
    def real(cls):
        return cls(wrap_driver_cls(AnfatecAMU24)())
