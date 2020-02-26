from lantz.qt import Backend, InstrumentSlot
from Model.AnfatecDriver import AnfatecAMU24


class LockinBackend(Backend):
    lockin: AnfatecAMU24 = InstrumentSlot

    def set_lockin_tc(self, num):
        self.lockin.time_constant = num

    def get_lockin_tc(self):
        return self.lockin.time_constant

    def set_lockin_rf(self, num):
        self.lockin.lockin_roll_off = num

    def get_lockin_rf(self):
        return self.lockin.lockin_roll_off

    def set_input_gain(self, num):
        self.lockin.input_gain = num

    def get_input_gain(self):
        return self.lockin.input_gain

    def set_coupling(self, coupling):
        self.lockin.coupling = coupling

    def get_coupling(self):
        return self.lockin.coupling

    def get_amplitude(self):
        self.log_debug('Updating Amplitude')
        return self.lockin.amplitude.magnitude

    def get_phase(self):
        self.log_debug('Updating Amplitude')
        return self.lockin.phase.magnitude

    def get_real_part(self):
        self.log_debug('Updating Amplitude')
        return self.lockin.real_part_x()

    def get_imaginary_part(self):
        self.log_debug('Updating Amplitude')
        return self.lockin.imaginary_part_y()

    def pll(self):
        return self.lockin.pll

    def toggle_pll(self):
        self.lockin.pll = not self.lockin.pll

    def overload(self):
        return self.lockin.overloaded

    def ext_frequency(self):
        return self.lockin.pll_frequency()
