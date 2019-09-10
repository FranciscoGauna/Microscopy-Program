from lantz import Feat
from lantz.core import foreign
from enum import Enum
from lantz import Q_


class Coupling(Enum):
    ac = 1
    dc = 0


class AnfatecAMU24(foreign.LibraryDriver):
    LIBRARY_NAME = "Lockin.dll"

    def __init__(self, *args, **kwargs):
        pll = kwargs.pop("pll", False) # False
        time_constant = (kwargs.pop("time_constant", 5))
        roll_off = (kwargs.pop("roll_off", 1))
        input_gain = kwargs.pop("input_gain", 1)
        harmonic = kwargs.pop("harmonic", 1)
        coupling = kwargs.pop("coupling", Coupling.dc)
        lockin_phase = Q_(kwargs.pop("lockin_phase", 45), "deg")
        lockin_amplitude = Q_(kwargs.pop("lockin_amplitude", 10), "V")
        lockin_frequency = Q_(kwargs.pop("lockin_frequency", 100), "hertz")

        super().__init__(library_name="Lockin.dll", *args, **kwargs)

        self._time_constant = 0
        self._roll_off = 0
        self.lib._GetLockInChannel.restype = foreign.TYPES["f64"]
        self.lib._GetLockInStatus.restype = foreign.TYPES["l"]
        self.lib._SetLockInPhase.restype = foreign.TYPES["f64"]
        self.lib._SetLockInPllOn.restype = foreign.TYPES["l"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]

        self.pll = pll
        self.set_lockin_time_constant(time_constant)
        self.set_lockin_time_constant(roll_off)
        self.input_gain = input_gain
        self.harmonic = harmonic
        self.coupling = coupling
        self.lockin_phase = lockin_phase
        self.lockin_amplitude = lockin_amplitude
        self.lockin_frequency = lockin_frequency

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
    def lockin_amplitude(self, value):
        """This Function sets the amplitude in V of the reference output and gives no value back"""
        self.lib._SetLockInAmpl(foreign.TYPES["f64"](value))
        self._lockin_amplitude = value

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
        self._harmonic = num
        self.lib._SetLockInHarm(foreign.TYPES["L"](num))

    def set_lockin_time_constant(self, num):
        if num not in range(0, 14):
            raise IndexError
        self._time_constant = num
        return self.lib._SetLockInTimeConst(foreign.TYPES["L"](num))

    def get_lockin_time_constant(self):
        # 0 = 0.25ms, 1 = 0.5ms, 2 = 1ms, 3 = 2ms, 4 = 5ms, ... 13 = 5s
        return self._time_constant

    def set_lockin_roll_off(self, num):
        if num not in range(0, 3):
            raise IndexError
        self._roll_off = num
        return self.lib._SetLockInRollOff(foreign.TYPES["L"](num))

    def get_lockin_roll_off(self):
        # 0 = 0.25ms, 1 = 0.5ms, 2 = 1ms, 3 = 2ms, 4 = 5ms, ... 13 = 5s
        return self._roll_off

    @Feat(units='V')
    def amplitude(self):
        return self.lib._GetLockInChannel(2)

    @Feat(units='degrees')
    def phase(self):
        return self.lib._GetLockInChannel(3)

    @Feat()
    def pll(self):
        return self._pll

    @pll.setter
    def pll(self, flag: bool):
        self._pll = flag
        num = 0
        if flag:
            num = 1
        self.lib._SetLockInPllOn(foreign.TYPES["l"](num))

    def pll_frequency(self):
        if self._pll:
            return self.lib._SetLockInFreq(foreign.TYPES["f64"](10.0))
        return 0

    @Feat()
    def status(self):
        return bool(self.lib._GetLockInStatus()-9)

    def real_part_x(self):
        return self.lib._GetLockInChannel(0)

    def imaginary_part_y(self):
        return self.lib._GetLockInChannel(1)

    def export_settings(self):
        settings = {
            "pll": self._pll,
            "time_constant": self._time_constant,
            "roll_off": self._roll_off,
            "input_gain": self._input_gain,
            "harmonic": self._harmonic,
            "coupling": self._coupling,
            "lockin_phase": self._lockin_phase,
            "lockin_amplitude": self._lockin_amplitude,
            "lockin_frequency": self._lockin_frequency,
        }

        return settings
