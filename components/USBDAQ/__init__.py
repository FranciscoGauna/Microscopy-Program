from SER.interfaces import Component
from lantz.qt import wrap_driver_cls

from .instrument_ui import DACInstrument, DACUI
from .USB2527 import USB2527, VirtualDAC


class USB2527DAC(Component):
    def __init__(self, DAC):
        self.instrument = DACInstrument(DAC)
        self.conf_ui = DACUI(backend=self.instrument)

    @classmethod
    def virtual(cls):
        return cls(VirtualDAC())

    @classmethod
    def real(cls, board_num):
        return cls(USB2527(board_num))

    def close_component(self):
        self.instrument.stop()
