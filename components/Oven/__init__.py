from SER.interfaces import Component
from lantz.qt import wrap_driver_cls

from .instrument_ui import OvenInstrument, OvenUI
from .TMS94 import T94Driver, VirtualOven


class LinkamOven(Component):
    def __init__(self, oven):
        self.instrument = OvenInstrument(oven=oven)
        self.conf_ui = OvenUI(backend=self.instrument)

    @classmethod
    def virtual(cls):
        return cls(wrap_driver_cls(VirtualOven)())

    @classmethod
    def real(cls, port):
        return cls(T94Driver.via_serial(port))
