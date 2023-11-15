from time import sleep
from typing import Dict, Any

from SER.interfaces import ObservableInstrument, ConfigurationUI
from lantz.qt import InstrumentSlot
from lantz.qt.connect import connect_feat

from .anfatec_driver import AnfatecAMU24


class Lockin(ObservableInstrument):
    lockin: AnfatecAMU24 = InstrumentSlot()

    def observe(self) -> Dict[str, Any]:
        # TODO: remove this
        self.lockin.lockin_frequency = 1000
        tc_time = float(self.lockin.time_constants.strip(" ms"))
        sleep(tc_time / 500)
        return {
            "amplitude": self.lockin.amplitude.magnitude,
            "phase": self.lockin.phase.magnitude
        }

    def get_config(self) -> Dict:
        """This function returns a dictionary of the values used for the configuration of the lockin. If you want to
         load a new instance with these setting you should add this dictionary to the kwargs when you instantiante the
         class"""
        settings = {
            "pll": self.lockin.pll,
            "time_constant": self.lockin.time_constants,
            "roll_off": self.lockin.lockin_roll_off,
            "sensitivity": self.lockin.sensitivity,
            "harmonic": self.lockin.harmonic,
            "coupling": self.lockin.coupling,
            "lockin_phase": self.lockin.lockin_phase.magnitude,
            "lockin_amplitude": self.lockin.lockin_amplitude.magnitude,
            "lockin_frequency": self.lockin.lockin_frequency.magnitude,
        }

        return settings


    def set_config(self, config: Dict):
        self.lockin.pll = config["pll"]
        self.lockin.time_constants = config["time_constant"]
        self.lockin.lockin_roll_off = config["roll_off"]
        self.lockin.sensitivity = config["sensitivity"]
        self.lockin.harmonic = config["harmonic"]
        self.lockin.coupling = config["coupling"]
        self.lockin.lockin_phase = config["lockin_phase"]
        self.lockin.lockin_amplitude = config["lockin_amplitude"]
        self.lockin.lockin_frequency = config["lockin_frequency"]

    def variable_documentation(self) -> Dict[str, str]:
        return {
            "amplitude": "Amplitude represents the amplitude measured from the given signal. As this instrument is "
                         "always connected with a reference, this should represent the full value of that function",
            "phase": "Phase represents the phase measured from the given signal. As this instrument is always connected"
                     "with a reference, this should represent the actual deviation from the original signal."
        }


class LockinUI(ConfigurationUI):
    gui = "conf.ui"

    backend: Lockin

    def __init__(self, backend):
        super().__init__(backend=backend)
        backend.initialize()
        connect_feat(self.widget.time_constant_cb, self.backend.lockin, "time_constants")
        connect_feat(self.widget.input_gain_cb, self.backend.lockin, "sensitivity")
        connect_feat(self.widget.slope_cb, self.backend.lockin, "lockin_roll_off")
        connect_feat(self.widget.harmonic_sb, self.backend.lockin, "harmonic")
        connect_feat(self.widget.pll_check, self.backend.lockin, "pll")
