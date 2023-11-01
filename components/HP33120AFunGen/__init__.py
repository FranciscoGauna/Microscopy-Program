from lantz.qt import wrap_driver_cls

from SER.interfaces import Component
from .instrument_ui import FunGen, FunGenConfUi
from .hp33120A_fungen import HP33120AFungen


class HPFunGen(Component):
    def __init__(self, address):
        fungen = wrap_driver_cls(HP33120AFungen).via_prologix_gpib(address)
        self.instrument = FunGen(fungen=fungen)
        self.conf_ui = FunGenConfUi(backend=self.instrument)
