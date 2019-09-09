from lantz import Feat
from lantz.core import foreign
from enum import Enum
from lantz import Q_


class Coupling(Enum):
    ac = 1
    dc = 0


class AnfatecAMU24(foreign.LibraryDriver):
    pll_status = True
    LIBRARY_NAME = "Lockin.dll"

    def __init__(self):
        super().__init__(library_name="Lockin.dll")

        self.lib._GetLockInChannel.restype = foreign.TYPES["f64"]
        self.lib._GetLockInStatus.restype = foreign.TYPES["l"]
        self.lib._SetLockInPhase.restype = foreign.TYPES["f64"]
        self.lib._SetLockInPllOn.restype = foreign.TYPES["l"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]

        self.lockin_phase = 45
        self.pll = False
        self.set_lockin_time_constant(5)
        self.input_gain = 10
        self.harmonic = 1
        self.coupling = Coupling.dc
        self.lockin_amplitude = Q_(10, "V")
        self.lockin_frequency = Q_(100.0, "hertz")

    @Feat(units="Hz")
    def lockin_frequency(self):
        """This Function sets the center frequency of the lockin to a value in Hz if the PLL is off. If the PLL is on,
        it returns the external frequency value"""
        return self._lockin_frequency

    @lockin_frequency.setter
    def lockin_frequency(self, float):
        """This Function sets the center frequency of the lockin to a value in Hz if the PLL is off. If the PLL is on,
        it returns the external frequency value"""
        self._lockin_frequency = float
        self.lib._SetLockInFreq(foreign.TYPES["f64"](float))

    @Feat(units="V")
    def lockin_amplitude(self):
        """This Function returns the amplitude in V of the reference output"""
        return self._lockin_amplitude

    @lockin_amplitude.setter
    def lockin_amplitude(self, float):
        """This Function sets the amplitude in V of the reference output and gives no value back"""
        self.lib._SetLockInAmpl(foreign.TYPES["f64"](float))
        self._lockin_amplitude = float

    @Feat(units="deg")
    def lockin_phase(self):
        return self._lockin_phase

    @lockin_phase.setter
    def lockin_phase(self, float):
        self._lockin_phase = float
        self.lib._SetLockInPhase(foreign.TYPES["f64"](float))

    @Feat
    def input_gain(self):
        return self._input_gain

    @input_gain.setter
    def input_gain(self, num):
        if num not in [1,10,100]:
            raise ValueError
        self._input_gain = num
        self.lib._SetLockInHardGain(foreign.TYPES["L"](num))

    @Feat
    def coupling(self):
        return self._coupling

    @coupling.setter
    def coupling(self, type: Coupling):
        if not isinstance(type, Coupling):
            raise TypeError()
        self._coupling = type
        self.lib._SetLockInCoupling(foreign.TYPES["L"](type.value))

    @Feat()
    def harmonic(self):
        return self.lib._SetLockInHarm()

    @harmonic.setter
    def harmonic(self, num):
        self._lockin_harmonic = num
        self.lib._SetLockInHarm(foreign.TYPES["L"](num))

    def set_lockin_time_constant(self, num):
        # 0 = 0.25ms, 1 = 0.5ms, 2 = 1ms, 3 = 2ms, 4 = 5ms, ... 13 = 5s
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
    def pll(self, flag: bool):
        self.pll_status = flag
        num = 0
        if flag:
            num = 1
        self.lib._SetLockInPllOn(foreign.TYPES["l"](num))

    def pll_frequency(self):
        if self.pll_status:
            return self.lib._SetLockInFreq(foreign.TYPES["f64"](10.0))
        return 0

    @Feat()
    def status(self):
        return bool(self.lib._GetLockInStatus()-9)
