from random import randrange, gauss
from time import sleep

from lantz import Feat
from lantz.core import foreign
from enum import Enum
from lantz import Q_
from os.path import dirname
from inspect import getfile


class VirtualLockin(foreign.Driver):

    def __init__(self, file=None, *args, **kwargs):
        """Instanciates a new copy of the driver. -if you want to load the settings of a previous instance of this class
        , you should use the method export_settings and add it to the kwargs"""
        reference_on = kwargs.pop("reference_on", False)
        time_constants = (kwargs.pop("time_constants", "5 ms"))
        roll_off = (kwargs.pop("roll_off", "12dB/oct"))
        input_gain = kwargs.pop("input_gain", "High Reserve")
        harmonic = kwargs.pop("harmonic", 1)
        coupling = kwargs.pop("coupling", "DC")
        reference_phase = Q_(kwargs.pop("reference_phase", 0), "deg")
        reference_amplitude = Q_(kwargs.pop("reference_amplitude", 1), "V")
        reference_frequency = Q_(kwargs.pop("reference_frequency", 10000), "hertz")

        super().__init__(*args, **kwargs)

        if file is not None:
            try:
                self.demo = []
                self.demo_amp_counter = 0
                self.demo_phase_counter = 0
                with open(file, 'r') as f:
                    for line in f:
                        self.demo.append(line.split(','))
            except FileNotFoundError:
                self.demo = None
        else:
            self.demo = None

        self.reference_on = reference_on
        self.time_constants = time_constants
        self.filter_slope = roll_off
        self.sensitivity = input_gain
        self.harmonic = harmonic
        self.coupling = coupling
        self.reference_phase = reference_phase
        self.reference_amplitude = reference_amplitude
        self.reference_frequency = reference_frequency

    @Feat(units="Hz")
    def reference_frequency(self):
        """This Function returns the center frequency of the lockin in Hz."""
        return self._reference_frequency

    @reference_frequency.setter
    def reference_frequency(self, float):
        """This Function sets the center frequency of the lockin to a value in Hz.
        It will only be used if the internal reference is off."""
        self._reference_frequency = float

    @Feat(units="V")
    def reference_amplitude(self):
        """This Function returns the amplitude in V of the reference output"""
        return self._reference_amplitude

    @reference_amplitude.setter
    def reference_amplitude(self, value):
        """This Function sets the amplitude in V of the reference output and gives no value back"""
        self._reference_amplitude = value

    @Feat(units="deg")
    def reference_phase(self):
        """This function returns the phase offset between the input and the reference output in degrees"""
        return self._reference_phase

    @reference_phase.setter
    def reference_phase(self, float):
        """This function sets the phase offset between the input and the reference output in degrees"""
        self._reference_phase = float

    @Feat(values={"High Reserve": 1, "Normal": 10, "Low Noise": 100})
    def sensitivity(self):
        """This function returns the input gain. It is a multiplier of either 1, 10 or 100"""
        return self._input_gain

    @sensitivity.setter
    def sensitivity(self, num):
        """This function sets the input gain. It is a multiplier of either 1, 10 or 100"""
        self._input_gain = num

    @Feat(values={"AC": 1, "DC": 0})
    def coupling(self):
        """This function returns the coupling gain"""
        return self._coupling

    @coupling.setter
    def coupling(self, coupling):
        """This function sets the coupling gain"""
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
    def filter_slope(self):
        """This function returns the roll off which is used for the low pass filter,
        assigned to each number: 0 = 6dB/oct, 1 = 12dB/oct, 2 = 24dB/oct"""
        return self._roll_off

    @filter_slope.setter
    def filter_slope(self, num):
        """This function sets the roll off which is used for the low pass filter
        , and it should be an integer between 0 and 2, with the following value.
        assigned to each number: 0 = 6dB/oct, 1 = 12dB/oct, 2 = 24dB/oct"""
        self._roll_off = num

    @Feat(units='V')
    def amplitude(self):
        """Returns the value of the amplitude channel, which measures from the input signal"""
        sleep(1)
        if self.demo and len(self.demo) > 0:
            val = self.demo[self.demo_amp_counter][0]
            self.demo_amp_counter += 1
            if self.demo_amp_counter >= len(self.demo):
                self.demo_amp_counter = 0
            return float(val)
        return randrange(200)

    @Feat(units='degrees')
    def phase(self):
        if self.demo and len(self.demo) > 0:
            val = self.demo[self.demo_phase_counter][1]
            self.demo_phase_counter += 1
            if self.demo_phase_counter >= len(self.demo):
                self.demo_phase_counter = 0
            return float(val)
        """phase returns the value of the phase channel, which measures from the input signal"""
        return gauss(50, 10)

    @Feat()
    def reference_on(self):
        """Returns a bool indicating if the internal reference is used.
        If true, the lockin uses the frequency of the external reference and if false it
        uses the internal value, assigned in reference_frequency"""
        return self._reference_on

    @reference_on.setter
    def reference_on(self, flag: bool):
        """Sets what frequency to use. If true, the lockin uses the frequency of the external reference and if false it
        uses the internal value, assigned in reference_frequency"""
        self._reference_on = flag

    @Feat()
    def overloaded(self):
        """Overloaded returns true when the lockin is overloaded and false when it is working correctly"""
        return False

    @Feat(units="V")
    def real_part_x(self):
        """Real Part x returns the value of the x channel , which measures from the input signal"""
        return 0

    @Feat(units="V")
    def imaginary_part_y(self):
        """Imaginaty part y returns the value of the x channel , which measures from the input signal"""
        return 0

    def export_settings(self) -> dict:
        """This function returns a dictionary of the values used for the configuration of the lockin. If you want to
         load a new instance with these setting you should add this dictionary to the kwargs when you instantiante the
         class"""
        settings = {
            "reference_on": self.reference_on,
            "time_constant": self.time_constant,
            "roll_off": self.filter_slope,
            "sensitivity": self.sensitivity,
            "harmonic": self.harmonic,
            "coupling": self.coupling,
            "reference_phase": self._reference_phase,
            "reference_amplitude": self._reference_amplitude,
            "reference_frequency": self._reference_frequency,
        }

        return settings


class AnfatecAMU24(foreign.LibraryDriver):
    LIBRARY_NAME = "Lockin.dll"

    def __init__(self, *args, **kwargs):
        """Instanciates a new copy of the driver. -if you want to load the settings of a previous instance of this class
        , you should use the method export_settings and add it to the kwargs"""
        # Popeo las variables que usa el programa
        reference_on = kwargs.pop("reference_on", False)
        time_constants = (kwargs.pop("time_constants", "5 ms"))
        roll_off = (kwargs.pop("roll_off", "12dB/oct"))
        input_gain = kwargs.pop("input_gain", "High Reserve")
        harmonic = kwargs.pop("harmonic", 1)
        coupling = kwargs.pop("coupling", "DC")
        reference_phase = Q_(kwargs.pop("reference_phase", 0), "deg")
        reference_amplitude = Q_(kwargs.pop("reference_amplitude", 1), "V")
        reference_frequency = Q_(kwargs.pop("reference_frequency", 10000), "hertz")

        super().__init__(library_name="Lockin.dll", library_folder=dirname(getfile(AnfatecAMU24)), *args, **kwargs)

        self._time_constant = 0
        self._roll_off = 0
        self.lib._GetLockInChannel.restype = foreign.TYPES["f64"]
        self.lib._GetLockInStatus.restype = foreign.TYPES["l"]
        self.lib._SetLockInPhase.restype = foreign.TYPES["f64"]
        self.lib._SetLockInPllOn.restype = foreign.TYPES["l"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]
        self.lib._SetLockInFreq.restype = foreign.TYPES["f64"]

        self.reference_on = reference_on
        self.time_constants = time_constants
        self.filter_slope = roll_off
        self.sensitivity = input_gain
        self.harmonic = harmonic
        self.coupling = coupling
        self.reference_phase = reference_phase
        self.reference_amplitude = reference_amplitude
        self.reference_frequency = reference_frequency

    @Feat(units="Hz")
    def reference_frequency(self):
        """This Function returns the center frequency of the lockin in Hz."""
        return self._reference_frequency

    @reference_frequency.setter
    def reference_frequency(self, float):
        """This Function sets the center frequency of the lockin to a value in Hz.
        It will only be used if the internal reference is off."""
        self._reference_frequency = float
        self.lib._SetLockInFreq(foreign.TYPES["f64"](float))

    @Feat(units="V")
    def reference_amplitude(self):
        """This Function returns the amplitude in V of the reference output"""
        return self._reference_amplitude

    @reference_amplitude.setter
    def reference_amplitude(self, value):
        """This Function sets the amplitude in V of the reference output and gives no value back"""
        self.lib._SetLockInAmpl(foreign.TYPES["f64"](value))
        self._reference_amplitude = value

    @Feat(units="deg")
    def reference_phase(self):
        """This function returns the phase offset between the input and the reference output in degrees"""
        return self._reference_phase

    @reference_phase.setter
    def reference_phase(self, float):
        """This function sets the phase offset between the input and the reference output in degrees"""
        self._reference_phase = float
        self.lib._SetLockInPhase(foreign.TYPES["f64"](float))

    @Feat(values={"High Reserve": 1, "Normal": 10, "Low Noise": 100})
    def sensitivity(self):
        """This function returns the input gain. It is a multiplier of either 1, 10 or 100"""
        return self._input_gain

    @sensitivity.setter
    def sensitivity(self, num):
        """This function sets the input gain. It is a multiplier of either 1, 10 or 100"""
        self._input_gain = num
        self.lib._SetLockInHardGain(foreign.TYPES["L"](num))

    @Feat(values={"AC": 1, "DC": 0})
    def coupling(self):
        """This function returns the coupling gain."""
        return self._coupling

    @coupling.setter
    def coupling(self, coupling):
        """This function sets the coupling gain."""
        self._coupling = coupling
        self.lib._SetLockInCoupling(foreign.TYPES["L"](coupling))

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
    def filter_slope(self):
        """This function returns the roll off which is used for the low pass filter
        ,
        assigned to each number: 0 = 6dB/oct, 1 = 12dB/oct, 2 = 24dB/oct"""
        return self._roll_off

    @filter_slope.setter
    def filter_slope(self, num):
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
    def reference_on(self):
        """Sets what frequency to use. If true, the lockin uses the frequency of the external reference and if false it
        uses the internal value, assigned in reference_frequency"""
        return self._reference_on

    @reference_on.setter
    def reference_on(self, flag: bool):
        """Sets what frequency to use. If true, the lockin uses the frequency of the external reference and if false it
        uses the internal value, assigned in reference_frequency"""
        self._reference_on = flag
        num = 0
        if flag:
            num = 1
        self.lib._SetLockInPllOn(foreign.TYPES["l"](num))

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

    def export_settings(self) -> dict:
        """This function returns a dictionary of the values used for the configuration of the lockin. If you want to
         load a new instance with these setting you should add this dictionary to the kwargs when you instantiante the
         class"""
        settings = {
            "reference_on": self.reference_on,
            "time_constant": self.time_constant,
            "roll_off": self.filter_slope,
            "sensitivity": self.sensitivity,
            "harmonic": self.harmonic,
            "coupling": self.coupling,
            "reference_phase": self._reference_phase,
            "reference_amplitude": self._reference_amplitude,
            "reference_frequency": self._reference_frequency,
        }

        return settings
