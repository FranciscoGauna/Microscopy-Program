from lantz import Feat
from lantz.core import foreign
from enum import Enum

class AnfatecAMU24(foreign.LibraryDriver):
    pll_status = True
    LIBRARY_NAME = "Lockin.dll"

    def __init__(self):
        super().__init__(library_name="Lockin.dll")

        self.lib._GetLockInChannel.restype = foreign.TYPES["f64"]
        self.lib._GetLockInStatus.restype = foreign.TYPES["L"]
        self.lib._SetLockInPhase.restype = foreign.TYPES["f64"]
        self.lib._SetLockInPllOn.restype = foreign.TYPES["L"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]

        self.pll = True
        self.set_lockin_time_constant(5)
        self.set_input_gain(10)
        self.harmonic = 1
        self.coupling = Coupling.ac
        self.lockin_amplitude_value = 0.0
        self.lockin_freq_value = 0.0

    @Feat()
    def lockin_frequency(self):
        """This Function sets the center frequency of the lockin to a value in Hz if the PLL is off. If the PLL is on,
        it returns the external frequency value"""
        return self.lib._SetLockInFreq()

    @lockin_frequency.setter
    def lockin_frequency(self, float):
        """This Function sets the center frequency of the lockin to a value in Hz if the PLL is off. If the PLL is on,
        it returns the external frequency value"""
        self.lib._SetLockInFreq(foreign.TYPES["f64"](float))

    @Feat()
    def lockin_amplitude(self):
        """This Function returns the amplitude in V of the reference output"""
        return self.lockin_amplitude_value

    @lockin_amplitude.setter
    def lockin_amplitude(self, float):
        """This Function sets the amplitude in V of the reference output and gives no value back"""
        self.lib._SetLockInAmpl(foreign.TYPES["f64"](float))
        self.lockin_amplitude_value = float

    def set_lockin_phase(self, float):
        return self.lib._SetLockInPhase(foreign.TYPES["f64"](float))

    def set_input_gain(self, num):
        return self.lib._SetLockInHardGain(foreign.TYPES["L"](num))

    @Feat
    def coupling(self):
        return self.lockin_coupling

    @coupling.setter
    def coupling(self, type: coupling):
        self.lockin_coupling = type
        self.lib._SetLockInCoupling(foreign.TYPES["L"](type.value))

    @Feat()
    def harmonic(self):
        return self.lib._SetLockInHarm()

    @harmonic.setter
    def harmonic(self, num):
        self.lockin_harmonic = num
        self.lib._SetLockInHarm(foreign.TYPES["L"](num))

    def set_lockin_time_constant(self, num):
        return self.lib._SetLockInTimeConst(foreign.TYPES["L"](num))

    @Feat(units='V')
    def amplitude(self):
        return self.lib._GetLockInChannel(2)

    @Feat(units='degrees')
    def phase(self):
        return self.lib._GetLockInChannel(3)

    @Feat()
    def pll(self):
        return self.pll_status

    @pll.setter
    def pll(self, bool):
        self.pll_status = bool
        num = 0
        if bool:
            num = 1
        self.lib._SetLockInPllOn(foreign.TYPES["L"](num))

    @Feat()
    def status(self):
        return self.lib._GetLockInStatus()


class Coupling(Enum):
    ac = 1
    dc = 0
