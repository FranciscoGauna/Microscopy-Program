import pyvisa
from lantz import MessageBasedDriver, Feat
from lantz.core.messagebased import get_resource_manager

from .dll_wrapper import FTD2XXWrapper


class HP33120AFungen(MessageBasedDriver):
    """Lantz Signal Generator.

    """

    PROLOGIX: bool  # This flag is used to indicate that we are using the gpib prologix adapter.
    PROLOGIX_ADDR: int  # The GPIB address to use if this is initialized with this addr

    DEFAULTS = {'COMMON': {'write_termination': '', 'read_termination': '\n'}}

    def __init__(self, resource_name, **kwargs):
        self.PROLOGIX = False
        self.initialized = False
        super().__init__(resource_name, **kwargs)
        self._shape = ""
        self._freq = 1.0
        self._amplitude = 1
        self._offset = 0

    @classmethod
    def via_prologix_gpib(cls, address):
        fungen = cls("dummy")
        fungen.PROLOGIX = True
        fungen.PROLOGIX_ADDR = address
        return fungen

    def initialize(self):

        if self.initialized:
            return

        super().initialize()
        if self.PROLOGIX:
            wrap = FTD2XXWrapper()
            # TODO: Fix this, it should know what is the prologix and/or taken an arg for the index
            self.resource = wrap.open(0, "\n", "")
            self.resource.set_timeout(100)
            self.resource.write(f"++addr {self.PROLOGIX_ADDR}")

            self._shape = self.shape
            self._freq = self.frequency.magnitude
            self._amplitude = self.amplitude.magnitude
            self._offset = self.offset.magnitude

        self.initialized = True

    def finalize(self):
        super().finalize()
        if self.PROLOGIX:
            del self.resource

    @Feat()
    def idn(self):
        return self.query('*IDN?')

    @Feat(values={"SIN", "SQU", "TRI", "RAMP", "NOIS", "DC", "USER"})
    def shape(self):
        return self.query("FUNCtion:SHAPe?")

    @shape.setter
    def shape(self, value):
        self._shape = value
        self.query(f"FUNCtion:SHAPe {value};*IDN?")

    @Feat(units="Hz", limits=(0.0001, 100000.0))
    def frequency(self):
        return float(self.query("FREQuency?"))

    @frequency.setter
    def frequency(self, value):
        self._freq = value
        self.query(f"FREQuency {value};*IDN?")

    @Feat(units="V", limits=(0.050, 10))
    def amplitude(self):
        return float(self.query("VOLTage?"))

    @amplitude.setter
    def amplitude(self, value):
        self._amplitude = value
        self.query(f"VOLTage {value};*IDN?")

    @Feat(units="V", limits=(-5, 5))
    def offset(self):
        return float(self.query("VOLTage:OFFSet?"))

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.query(f"VOLTage:OFFSet {value};*IDN?")

    def apply(self, shape=None, freq=None, amplitude=None, offset=None):
        shape = self._shape if shape is None else shape
        freq = self._freq if freq is None else freq
        amplitude = self._amplitude if amplitude is None else amplitude
        offset = self._offset if offset is None else offset

        self.query(f":APPL:{shape} {freq}Hz, {amplitude}V, {offset}V;*IDN?")


if __name__ == "__main__":
    test_dev = HP33120AFungen.via_prologix_gpib(10)
    test_dev.initialize()
    test_dev.apply(shape="SIN", freq=9430.0, amplitude=1.5)
