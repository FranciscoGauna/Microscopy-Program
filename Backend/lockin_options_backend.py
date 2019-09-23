from lantz.qt import Backend, InstrumentSlot
from Model.AnfatecDriver import AnfatecAMU24


class LockinControl(Backend):
    lockin: AnfatecAMU24 = InstrumentSlot

    def set_lockin_tc(self, num):
        self.lockin.set_lockin_time_constant(num)

    def get_lockin_tc(self):
        return self.lockin.get_lockin_time_constant()

    def set_lockin_rf(self, num):
        self.lockin.lockin_roll_off = num

    def get_lockin_rf(self):
        return self.lockin.lockin_roll_off


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
