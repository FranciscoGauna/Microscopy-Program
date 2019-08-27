from lantz.qt.app import start_gui
from lantz.core import foreign


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
        self.set_pll(True)

    def set_pll(self, bool):
        self.pll_status = bool
        num = 0
        if bool:
            num = 1
        return self.lib._SetLockInPllOn(foreign.TYPES["L"](num))

    def set_lockin_freq(self, float):
        """This Function sets the center frequency of the lockin to a value in Hz if the PLL is off. If the PLL is on,
        it returns the external frequency value"""
        return self.lib._SetLockInFreq(foreign.TYPES["f64"](float))

    def set_lockin_amplitude(self, float):
        self.lib._SetLockInAmpl(foreign.TYPES["f64"](float))
        return None

    def set_lockin_phase(self, float):
        return self.lib._SetLockInPhase(foreign.TYPES["f64"](float))

    def set_input_gain(self, num):
        return self.lib._SetLockInHardGain(foreign.TYPES["L"](num))

    def set_lockin_coupling(self, num):
        return self.lib._SetLockInCoupling(foreign.TYPES["L"](num))

    def set_lockin_harmonic(self, num):
        return self.lib._SetLockInHarm(foreign.TYPES["L"](num))

    def set_lockin_time_constant(self, num):
        return self.lib._SetLockInTimeConst(foreign.TYPES["L"](num))

    def get_amplitude(self):
        return self.lib._GetLockInChannel(2)

    def get_phase(self):
        return self.lib._GetLockInChannel(3)

    def get_pll_status(self):
        return self.pll_status

    def get_lockin_status(self):
        return self.lib._GetLockInStatus()
