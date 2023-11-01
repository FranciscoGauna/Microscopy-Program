from typing import Dict, Generator, Any

from PyQt5.QtWidgets import QDoubleSpinBox, QComboBox
from lantz.qt import InstrumentSlot
from lantz.qt.connect import connect_feat

from .hp33120A_fungen import HP33120AFungen
from SER.interfaces import ConfigurableInstrument, ConfigurationUI


class FunGen(ConfigurableInstrument):
    fungen: HP33120AFungen = InstrumentSlot()

    def configure(self, shape, freq, amplitude, offset) -> Dict[str, Any]:
        # This is the function would do in an environment with multiple configs
        # self.fungen.apply(shape, freq, amplitude, offset)
        return {
            "shape": shape,
            "frequency": freq,
            "amplitude": amplitude,
            "offset": offset
        }

    def get_points(self) -> Generator:
        # We have a scenario where it's already configured in the gui
        yield (self.fungen.shape, self.fungen.frequency.magnitude, self.fungen.amplitude.magnitude,
               self.fungen.offset.magnitude)

    def point_amount(self) -> int:
        return 1

    def get_config(self) -> Dict:
        return {
            "shape": self.fungen.shape,
            "frequency": self.fungen.frequency.magnitude,
            "amplitude": self.fungen.amplitude.magnitude,
            "offset": self.fungen.offset.magnitude
        }

    def set_config(self, config: Dict):
        self.fungen.shape = config["shape"]
        self.fungen.frequency = config["frequency"]
        self.fungen.amplitude = config["amplitude"]
        self.fungen.offset = config["offset"]

    def variable_documentation(self) -> Dict[str, str]:
        return {

        }


class FunGenConfUi(ConfigurationUI):
    gui = (".", "conf_ui.ui")
    backend: FunGen

    def __init__(self, backend):
        super().__init__(backend=backend)
        backend.initialize()
        connect_feat(self.widget.shape_cb, self.backend.fungen, "shape")
        connect_feat(self.widget.frequency_sb, self.backend.fungen, "frequency")
        connect_feat(self.widget.amplitude_sb, self.backend.fungen, "amplitude")
        connect_feat(self.widget.offset_sb, self.backend.fungen, "offset")
