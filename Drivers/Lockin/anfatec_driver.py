from random import randrange, gauss

from lantz import Feat
from lantz.core import foreign
from enum import Enum
from lantz import Q_
from os.path import dirname
from inspect import getfile


class Coupling(Enum):
    ac = 1
    dc = 0


class VirtualLockin(foreign.Driver):

    def __init__(self, *args, **kwargs):
        """Instanciates a new copy of the driver. -if you want to load the settings of a previous instance of this class
        , you should use the method export_settings and add it to the kwargs"""
        pll = kwargs.pop("pll", False)
        time_constant = (kwargs.pop("time_constant", "5 ms"))
        roll_off = (kwargs.pop("roll_off", "12dB/oct"))
        input_gain = kwargs.pop("input_gain", 1)
        harmonic = kwargs.pop("harmonic", 1)
        coupling = kwargs.pop("coupling", Coupling.dc)
        lockin_phase = Q_(kwargs.pop("lockin_phase", 0), "deg")
        lockin_amplitude = Q_(kwargs.pop("lockin_amplitude", 1), "V")
        lockin_frequency = Q_(kwargs.pop("lockin_frequency", 10000), "hertz")

        super().__init__(*args, **kwargs)

        self._time_constant = 0
        self._roll_off = 0
        self._input_gain = 1

        self.pll = pll
        self.time_constant = time_constant
        self.lockin_roll_off = roll_off
        self.input_gain = input_gain
        self.harmonic = harmonic
        self.coupling = coupling
        self.lockin_phase = lockin_phase
        self.lockin_amplitude = lockin_amplitude
        self.lockin_frequency = lockin_frequency

    @Feat(units="Hz")
    def lockin_frequency(self):
        """This Function returns the center frequency of the lockin in Hz."""
        return self._lockin_frequency

    @lockin_frequency.setter
    def lockin_frequency(self, float):
        """This Function sets the center frequency of the lockin to a value in Hz. It will only be used if the PLL is off."""
        self._lockin_frequency = float

    @Feat(units="V")
    def lockin_amplitude(self):
        """This Function returns the amplitude in V of the reference output"""
        return self._lockin_amplitude

    @lockin_amplitude.setter
    def lockin_amplitude(self, value):
        """This Function sets the amplitude in V of the reference output and gives no value back"""
        self._lockin_amplitude = value

    @Feat(units="deg")
    def lockin_phase(self):
        """This function returns the phase offset between the input and the reference output in degrees"""
        return self._lockin_phase

    @lockin_phase.setter
    def lockin_phase(self, float):
        """This function sets the phase offset between the input and the reference output in degrees"""
        self._lockin_phase = float

    @Feat(values={1, 10, 100})
    def sensitivity(self):
        """This function returns the input gain. It is a multiplier of either 1, 10 or 100"""
        return self._input_gain

    @sensitivity.setter
    def sensitivity(self, num):
        """This function sets the input gain. It is a multiplier of either 1, 10 or 100"""
        self._input_gain = num

    @Feat(values={Coupling.ac, Coupling.dc})
    def coupling(self):
        """This function returns the coupling gain. It returns an instance of the Coupling Enum Class"""
        return self._coupling

    @coupling.setter
    def coupling(self, coupling: Coupling):
        """This function sets the coupling gain. It requires an instance of the Coupling Enum Class"""
        if not isinstance(coupling, Coupling):
            raise TypeError()
        self._coupling = coupling

    @Feat(values=set(range(0, 16)))
    def harmonic(self):
        """This function returns the harmonic, an integer between 1 and 15"""
        return self._harmonic

    @harmonic.setter
    def harmonic(self, num):
        """This function sets the harmonic, and it should be an integer between 1 and 15"""
        self._harmonic = num

    @Feat(values={"0.25 ms": 0, "0.5 ms": 1, "1 ms": 2, "2 ms": 3, "5 ms": 4,  "10 ms": 5,  "20 ms": 6,  "50 ms": 7,
                  "100 ms": 8,  "200 ms": 9, "500 ms": 10,  "1000 ms": 11,  "2000 ms": 12, "5000 ms": 13})
    def time_constants(self):
        """This function sets the time constant that the lockin uses for integration,
         and it should be an integer between 0 and 13, with the following value
        assigned to each number: 0 = 0.25ms, 1 = 0.5ms, 2 = 1ms, 3 = 2ms, 4 = 5ms, ... 13 = 5s"""
        # 0 = 0.25ms, 1 = 0.5ms, 2 = 1ms, 3 = 2ms, 4 = 5ms, ... 13 = 5s
        return self._time_constant

    @time_constants.setter
    def time_constants(self, num):
        """This function sets the time constant that the lockin uses for integration,
        and it should be an integer between 0 and 13, with the following value
        assigned to each number: 0 = 0.25ms, 1 = 0.5ms, 2 = 1ms, 3 = 2ms, 4 = 5ms, ... 13 = 5s"""
        self._time_constant = num

    @Feat(values={"6dB/oct": 0, "12dB/oct": 1, "24dB/oct": 2})
    def filter_db_per_oct(self):
        """This function returns the roll off which is used for the low pass filter
        ,
        assigned to each number: 0 = 6dB/oct, 1 = 12dB/oct, 2 = 24dB/oct"""
        return self._roll_off

    @filter_db_per_oct.setter
    def filter_db_per_oct(self, num):
        """This function sets the roll off which is used for the low pass filter
        , and it should be an integer between 0 and 2, with the following value.
        assigned to each number: 0 = 6dB/oct, 1 = 12dB/oct, 2 = 24dB/oct"""
        self._roll_off = num

    @Feat(units='V')
    def amplitude(self):
        """Returns the value of the amplitude channel, which measures from the input signal"""
        return randrange(200)

    @Feat(units='degrees')
    def phase(self):
        """phase returns the value of the phase channel, which measures from the input signal"""
        return gauss(50, 10)

    @Feat()
    def pll(self):
        """Returns the value of pll. If true, the lockin uses the frequency of the external reference and if false it
        uses the internal value, assigned in lockin_frequency"""
        return self._pll

    @pll.setter
    def pll(self, flag: bool):
        """Sets what frequency to use. If true, the lockin uses the frequency of the external reference and if false it
        uses the internal value, assigned in lockin_frequency"""
        self._pll = flag
        num = 0
        if flag:
            num = 1

    def pll_frequency(self):
        """Returns the fequency of the pll if the pll is on. Otherwise returns 0"""
        return 0.0

    @Feat()
    def overloaded(self):
        """Overloaded returns true when the lockin is overloaded and false when it is working correctly"""
        return False

    def real_part_x(self):
        """Real Part x returns the value of the x channel , which measures from the input signal"""
        return 0

    def imaginary_part_y(self):
        """Imaginaty part y returns the value of the x channel , which measures from the input signal"""
        return 0


class AnfatecAMU24(foreign.LibraryDriver):
    LIBRARY_NAME = "Lockin.dll"

    def __init__(self, *args, **kwargs):
        """Instanciates a new copy of the driver. -if you want to load the settings of a previous instance of this class
        , you should use the method export_settings and add it to the kwargs"""
        # Popeo las variables que usa el programa
        pll = kwargs.pop("pll", False)
        time_constants = (kwargs.pop("time_constants", "5 ms"))
        roll_off = (kwargs.pop("roll_off", "12dB/oct"))
        input_gain = kwargs.pop("input_gain", 1)
        harmonic = kwargs.pop("harmonic", 1)
        coupling = kwargs.pop("coupling", Coupling.dc)
        lockin_phase = Q_(kwargs.pop("lockin_phase", 0), "deg")
        lockin_amplitude = Q_(kwargs.pop("lockin_amplitude", 1), "V")
        lockin_frequency = Q_(kwargs.pop("lockin_frequency", 10000), "hertz")

        super().__init__(library_name="Lockin.dll", library_folder=dirname(getfile(AnfatecAMU24)), *args, **kwargs)

        self._time_constant = 0
        self._roll_off = 0
        self.lib._GetLockInChannel.restype = foreign.TYPES["f64"]
        self.lib._GetLockInStatus.restype = foreign.TYPES["l"]
        self.lib._SetLockInPhase.restype = foreign.TYPES["f64"]
        self.lib._SetLockInPllOn.restype = foreign.TYPES["l"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]

        self.pll = pll
        self.time_constant = time_constants
        self.lockin_roll_off = roll_off
        self.input_gain = input_gain
        self.harmonic = harmonic
        self.coupling = coupling
        self.lockin_phase = lockin_phase
        self.lockin_amplitude = lockin_amplitude
        self.lockin_frequency = lockin_frequency

    @Feat(units="Hz")
    def lockin_frequency(self):
        """This Function returns the center frequency of the lockin in Hz."""
        return self._lockin_frequency

    @lockin_frequency.setter
    def lockin_frequency(self, float):
        """This Function sets the center frequency of the lockin to a value in Hz. It will only be used if the PLL is
        off."""
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
        """This function returns the phase offset between the input and the reference output in degrees"""
        return self._lockin_phase

    @lockin_phase.setter
    def lockin_phase(self, float):
        """This function sets the phase offset between the input and the reference output in degrees"""
        self._lockin_phase = float
        self.lib._SetLockInPhase(foreign.TYPES["f64"](float))

    @Feat(values={1, 10, 100})
    def sensitivity(self):
        """This function returns the input gain. It is a multiplier of either 1, 10 or 100"""
        return self._input_gain

    @sensitivity.setter
    def sensitivity(self, num):
        """This function sets the input gain. It is a multiplier of either 1, 10 or 100"""
        self._input_gain = num
        self.lib._SetLockInHardGain(foreign.TYPES["L"](num))

    @Feat(values={Coupling.ac, Coupling.dc})
    def coupling(self):
        """This function returns the coupling gain. It returns an instance of the Coupling Enum Class"""
        return self._coupling

    @coupling.setter
    def coupling(self, coupling: Coupling):
        """This function sets the coupling gain. It requires an instance of the Coupling Enum Class"""
        if not isinstance(coupling, Coupling):
            raise TypeError()
        self._coupling = coupling
        self.lib._SetLockInCoupling(foreign.TYPES["L"](coupling.value))

    @Feat(values=set(range(0, 16)))
    def harmonic(self):
        """This function returns the harmonic, an integer between 1 and 15"""
        return self._harmonic

    @harmonic.setter
    def harmonic(self, num):
        """This function sets the harmonic, and it should be an integer between 1 and 15"""
        self._harmonic = num
        self.lib._SetLockInHarm(foreign.TYPES["L"](num))

    @Feat(values={"0.25 ms": 0, "0.5 ms": 1, "1 ms": 2, "2 ms": 3, "5 ms": 4,  "10 ms": 5,  "20 ms": 6,  "50 ms": 7,
                  "100 ms": 8,  "200 ms": 9, "500 ms": 10,  "1000 ms": 11,  "2000 ms": 12, "5000 ms": 13})
    def time_constants(self):
        """This function sets the time constant that the lockin uses for integration,
         and it should be an integer between 0 and 13, with the following value
        assigned to each number: 0 = 0.25ms, 1 = 0.5ms, 2 = 1ms, 3 = 2ms, 4 = 5ms, ... 13 = 5s"""
        # 0 = 0.25ms, 1 = 0.5ms, 2 = 1ms, 3 = 2ms, 4 = 5ms, ... 13 = 5s
        return self._time_constant

    @time_constants.setter
    def time_constants(self, num):
        """This function sets the time constant that the lockin uses for integration,
        and it should be an integer between 0 and 13, with the following value
        assigned to each number: 0 = 0.25ms, 1 = 0.5ms, 2 = 1ms, 3 = 2ms, 4 = 5ms, ... 13 = 5s"""
        self._time_constant = num
        self.lib._SetLockInTimeConst(foreign.TYPES["L"](num))

    @Feat(values={"6dB/oct": 0, "12dB/oct": 1, "24dB/oct": 2})
    def lockin_roll_off(self):
        """This function returns the roll off which is used for the low pass filter
        ,
        assigned to each number: 0 = 6dB/oct, 1 = 12dB/oct, 2 = 24dB/oct"""
        return self._roll_off

    @lockin_roll_off.setter
    def lockin_roll_off(self, num):
        """This function sets the roll off which is used for the low pass filter
        , and it should be an integer between 0 and 2, with the following value.
        assigned to each number: 0 = 6dB/oct, 1 = 12dB/oct, 2 = 24dB/oct"""
        self._roll_off = num
        self.lib._SetLockInRollOff(foreign.TYPES["L"](num))

    @Feat(units='V')
    def amplitude(self):
        """Returns the value of the amplitude channel, which measures from the input signal"""
        return self.lib._GetLockInChannel(2)

    @Feat(units='degrees')
    def phase(self):
        """phase returns the value of the phase channel, which measures from the input signal"""
        return self.lib._GetLockInChannel(3)

    @Feat()
    def pll(self):
        """Returns the value of pll. If true, the lockin uses the frequency of the external reference and if false it
        uses the internal value, assigned in lockin_frequency"""
        return self._pll

    @pll.setter
    def pll(self, flag: bool):
        """Sets what frequency to use. If true, the lockin uses the frequency of the external reference and if false it
        uses the internal value, assigned in lockin_frequency"""
        self._pll = flag
        num = 0
        if flag:
            num = 1
        self.lib._SetLockInPllOn(foreign.TYPES["l"](num))

    def pll_frequency(self):
        """Returns the fequency of the pll if the pll is on. Otherwise returns 0"""
        if self._pll:
            return self.lib._SetLockInFreq(foreign.TYPES["f64"](10.0))
        return 0.0

    @Feat()
    def overloaded(self):
        """Overloaded returns true when the lockin is overloaded and false when it is working correctly"""
        return bool(self.lib._GetLockInStatus()-9)

    def real_part_x(self):
        """Real Part x returns the value of the x channel , which measures from the input signal"""
        return self.lib._GetLockInChannel(0)

    def imaginary_part_y(self):
        """Imaginaty part y returns the value of the x channel , which measures from the input signal"""
        return self.lib._GetLockInChannel(1)

    def export_settings(self):
        """This function returns a dictionary of the values used for the configuration of the lockin. If you want to
         load a new instance with these setting you should add this dictionary to the kwargs when you instantiante the
         class"""
        settings = {
            "pll": self._pll,
            "time_constant": self.time_constant,
            "roll_off": self.lockin_roll_off,
            "input_gain": self._input_gain,
            "harmonic": self._harmonic,
            "coupling": self._coupling,
            "lockin_phase": self._lockin_phase,
            "lockin_amplitude": self._lockin_amplitude,
            "lockin_frequency": self._lockin_frequency,
        }

        return settings
