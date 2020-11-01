from lantz.qt import Backend, InstrumentSlot
from Drivers.Lockin.anfatec_driver import AnfatecAMU24


class LockinBackend(Backend):
    lockin: AnfatecAMU24

    def __init__(self, lockin, **instruments_and_backends):
        self.lockin = lockin
        super().__init__(**instruments_and_backends)

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
        return self.lockin.amplitude.magnitude

    def get_phase(self):
        return self.lockin.phase.magnitude

    def get_real_part(self):
        return self.lockin.real_part_x.magnitude

    def get_imaginary_part(self):
        return self.lockin.imaginary_part_y.magnitude

    def pll(self):
        return self.lockin.reference_internal

    def toggle_pll(self):
        self.lockin.reference_internal = not self.lockin.reference_internal

    def overload(self):
        try:
            return self.lockin.overloaded
        except:
            return False

    def ext_frequency(self):
        return self.lockin.frequency.magnitude
