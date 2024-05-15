from time import sleep
from typing import Dict, Any

from SER.interfaces import ObservableInstrument, ConfigurationUI
from lantz.qt import InstrumentSlot
from lantz.qt.connect import connect_feat

from .anfatec_driver import AnfatecAMU24


class Lockin(ObservableInstrument):
    lockin: AnfatecAMU24 = InstrumentSlot()

    def observe(self) -> Dict[str, Any]:
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
            "reference_on": self.lockin.reference_on,
            "time_constant": self.lockin.time_constants,
            "filter_slope": self.lockin.filter_slope,
            "sensitivity": self.lockin.sensitivity,
            "harmonic": self.lockin.harmonic,
            "coupling": self.lockin.coupling,
            "reference_phase": self.lockin.reference_phase.magnitude,
            "reference_amplitude": self.lockin.reference_amplitude.magnitude,
            "reference_frequency": self.lockin.reference_frequency.magnitude,
        }

        return settings

    def set_config(self, config: Dict):
        self.lockin.reference_on = config["reference_on"]
        self.lockin.time_constants = config["time_constant"]
        self.lockin.filter_slope = config["filter_slope"]
        self.lockin.sensitivity = config["sensitivity"]
        self.lockin.harmonic = config["harmonic"]
        self.lockin.coupling = config["coupling"]
        self.lockin.reference_phase = config["reference_phase"]
        self.lockin.reference_amplitude = config["reference_amplitude"]
        self.lockin.reference_frequency = config["reference_frequency"]

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
        connect_feat(self.widget.slope_cb, self.backend.lockin, "filter_slope")
        connect_feat(self.widget.harmonic_sb, self.backend.lockin, "harmonic")
        connect_feat(self.widget.pll_check, self.backend.lockin, "reference_on")
