from typing import Dict, Any

from SER.interfaces import ObservableInstrument, ConfigurationUI
from lantz.qt import InstrumentSlot
from lantz.qt.connect import connect_feat

from .anfatec_driver import AnfatecAMU24


class Lockin(ObservableInstrument):
    lockin: AnfatecAMU24 = InstrumentSlot()

    def observe(self) -> Dict[str, Any]:
        return {
            "amplitude": self.lockin.amplitude.magnitude,
            "phase": self.lockin.phase.magnitude
        }

    def get_config(self) -> Dict:
        pass

    def set_config(self, config: Dict):
        pass

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
