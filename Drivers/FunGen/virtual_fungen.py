from lantz import Feat
from lantz import Driver


class VirtualFungen(Driver):

    @Feat()
    def idn(self):
        return 0

    @Feat(units="Hz", limits=(1e-6, 25e6))
    def frequency(self):
        """
        Returns the frequency of the specified channel, in Hertz.
        """
    @frequency.setter
    def frequency(self, value):
        """
        Sets the frequency of the specified channel, to value. Note that this
        is not smart enough to keep track of the different bandwidth constraints
        on different types of waveforms, so see the manual accordingly.
        """

    @Feat()
    def function(self):
        """
        Returns the function of the specified channel from the options
        enumerated in WAVEFORMS.
        """

    @function.setter
    def function(self, value):
        """
        Returns the function of the specified channel to value (specified in
        WAVEFORMS).
        """

    @Feat()
    def output(self, channel):
        """
        Reads the output state of the specified channel.
        """

    @output.setter
    def output(self, channel, val):
        """
        Sets the output state of the specified channel to val.
        """

    @Feat(units="V", limits=(-10., 10.))
    def voltage_low(self, channel):
        """
        Queries the low voltage level for the specified channel.
        """

    @voltage_low.setter
    def voltage_low(self, channel, value):
        """
        Sets the high voltage level for the specified channel.
        """

    @Feat(units="V", limits=(-10., 10.))
    def voltage_high(self, channel):
        """
        Queries the high voltage level for the specified channel.
        """

    @voltage_high.setter
    def voltage_high(self, channel, value):
        """
        Sets the high voltage level for the specified channel.
        """

    @Feat(units="V", limits=(0., 20.))
    def voltage_amplitude(self, channel):
        """
        Queries the peak-to-peak voltage amplitude of the specified output
        channel.
        """

    @voltage_amplitude.setter
    def voltage_amplitude(self, value):
        """
        Sets the peak-to-peak voltage amplitude of the specified output channel.
        """

    @Feat(units="V", limits=(-10., 10.))
    def voltage_offset(self):
        """
        Queries the offset voltage of the specified output channel.
        """

    @voltage_offset.setter
    def voltage_offset(self, value):
        """
        Sets the offset voltage of the specified output channel.
        """
