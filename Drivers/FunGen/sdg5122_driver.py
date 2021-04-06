from datetime import datetime, timedelta

from lantz import Feat, Action, DictFeat
from lantz.core.messagebased import MessageBasedDriver


class SDG5122(MessageBasedDriver):
    """
    Class that administers and provides an interface to connect with the function generator SDG5122 from Siglent
    """

    DEFAULTS = {
        'COMMON': {
            'write_termination': '\n',
            'read_termination': '\n',
        }
    }

    _state = {
        1: {
            "WVTP": "",
            "FRQ": "",
            "PERI": "",
            "AMP": "",
            "OFST": "",
            "HLEV": "",
            "LLEV": "",
            "PHSE": ""
        },
        2: {
            "WVTP": "",
            "FRQ": "",
            "PERI": "",
            "AMP": "",
            "OFST": "",
            "HLEV": "",
            "LLEV": "",
            "PHSE": ""
        }
    }

    _state_time = {
        1: datetime.now(),
        2: datetime.now()
    }

    CHANNELS = dict([(1, 1),
                     (2, 2)])

    TOGGLE = dict([('on', 'ON'),
                   ('off', 'OFF')])

    WAVEFORMS = dict([('arbitrary', 'ARB'),
                      ('dc', 'DC'),
                      ('sin', 'SINE'),
                      ('harmonic', 'HARM'),
                      ('noise', 'NOISE'),
                      ('pulse', 'PULSE'),
                      ('ramp', 'RAMP'),
                      ('square', 'SQUARE')])

    def initialize(self):
        super().initialize()

    # Example command: BSWV?
    # Return: BSWV WVTP,SINE,FRQ,100HZ,PERI,0.01S,AMP,2V,OFST,0V,HLEV,1V,LLEV,-1V,PHSE,0
    def refresh_state(self):
        """
        Refreshes the state of the data stored about the device.
        :return: none
        """
        result_1 = self.query('1:BSWV?')[5:].split(',')
        result_2 = self.query('2:BSWV?')[5:].split(',')
        result_1 = [(result_1[i * 2], result_1[i * 2 + 1]) for i in range(len(result_1) // 2)]
        result_2 = [(result_2[i * 2], result_2[i * 2 + 1]) for i in range(len(result_2) // 2)]
        self._state[1] = dict(result_1)
        self._state[2] = dict(result_2)

    def get_state(self, channel, type):
        if (datetime.now() - self._state_time[channel]) > timedelta(seconds=0.5):
            self.refresh_state()
            self._state_time[channel] = datetime.now()
        return self._state[channel][type]

    @Feat(read_once=True)
    def idn(self):
        """
        The ❊IDN? query returns the SR830's device identification string. This
        string is in the format
        "Stanford_Research_Systems,SR830,s/n00111,ver1.000".
        :return: Identification string
        """
        return self.query('*IDN?')

    @Action()
    def reset(self):
        return self.write('*RST')

    @DictFeat(keys=CHANNELS, units="Hz", limits=(1e-6, 25e6))
    def frequency(self, channel):
        """
        Returns the frequency of the specified channel, in Hertz.
        """
        return self.get_state(channel, "FRQ")

    @frequency.setter
    def frequency(self, channel, value):
        """
        Sets the frequency of the specified channel, to value. Note that this
        is not smart enough to keep track of the different bandwidth constraints
        on different types of waveforms, so see the manual accordingly.
        """
        self.write('{}:BSWV FRQ, {}'.format(channel, value))

    @DictFeat(keys=CHANNELS, values=WAVEFORMS)
    def function(self, channel):
        """
        Returns the function of the specified channel from the options
        enumerated in WAVEFORMS.
        """
        return self.get_state(channel, "WVTP")

    @function.setter
    def function(self, channel, value):
        """
        Sets the function of the specified channel to value (specified in
        WAVEFORMS).
        """
        self.write('{}:BSWV WVTP, {}'.format(channel, value))

    @DictFeat(keys=CHANNELS, units="V", limits=(-10., 10.))
    def voltage_low(self, channel):
        """
        Queries the low voltage level for the specified channel.
        """
        return self.get_state(channel, "LLEV")

    @voltage_low.setter
    def voltage_low(self, channel, value):
        """
        Sets the high voltage level for the specified channel.
        """
        self.write('{}:BSWV LLEV, {}'.format(channel, value))

    @DictFeat(keys=CHANNELS, units="V", limits=(-10., 10.))
    def voltage_high(self, channel):
        """
        Queries the high voltage level for the specified channel.
        """
        return self.get_state(channel, "HLEV")

    @voltage_high.setter
    def voltage_high(self, channel, value):
        """
        Sets the high voltage level for the specified channel.
        """
        self.write('{}:BSWV HLEV, {}'.format(channel, value))

    @DictFeat(keys=CHANNELS, units="V", limits=(0., 20.))
    def voltage_amplitude(self, channel):
        """
        Queries the peak-to-peak voltage amplitude of the specified output
        channel.
        """
        return self.get_state(channel, "AMP")

    @voltage_amplitude.setter
    def voltage_amplitude(self, channel, value):
        """
        Sets the peak-to-peak voltage amplitude of the specified output channel.
        """
        self.write('{}:BSWV AMP, {}'.format(channel, value))

    @DictFeat(keys=CHANNELS, units="V", limits=(-10., 10.))
    def voltage_offset(self, channel):
        """
        Queries the offset voltage of the specified output channel.
        """
        return self.get_state(channel, "OFST")

    @voltage_offset.setter
    def voltage_offset(self, channel, value):
        """
        Sets the offset voltage of the specified output channel.
        """
        self.write('{}:BSWV OFST, {}'.format(channel, value))
