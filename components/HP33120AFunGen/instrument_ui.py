import math
from typing import Dict, Generator, Any

from PyQt5.QtWidgets import QDoubleSpinBox, QComboBox
from lantz import Feat
from lantz.qt import InstrumentSlot
from lantz.qt.connect import connect_feat

from .hp33120A_fungen import HP33120AFungen
from SER.interfaces import ConfigurableInstrument, ConfigurationUI


class FunGen(ConfigurableInstrument):
    fungen: HP33120AFungen = InstrumentSlot()

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)

        self._shape = "SIN"
        self._amplitude = 2.5
        self._offset = 0.0
        self._amount_frequency = 2
        self._min_frequency = 1.0
        self._max_frequency = 2.0
        self._log = False

    def configure(self, shape, freq, amplitude, offset) -> Dict[str, Any]:
        self.fungen.apply(shape, freq, amplitude, offset)
        return {
            "shape": shape,
            "frequency": freq,
            "amplitude": amplitude,
            "offset": offset
        }

    @Feat(values={"SIN", "SQU", "TRI", "RAMP", "NOIS", "DC", "USER"})
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = value

    @Feat
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value):
        self._amplitude = value

    @Feat
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @Feat
    def log_scale(self):
        return self._log

    @log_scale.setter
    def log_scale(self, value):
        self._log = value

    @Feat
    def amount_frequency(self):
        return self._amount_frequency

    @amount_frequency.setter
    def amount_frequency(self, value):
        self._amount_frequency = value

    @Feat
    def min_frequency(self):
        return self._min_frequency

    @min_frequency.setter
    def min_frequency(self, value):
        self._min_frequency = value

    @Feat
    def max_frequency(self):
        return self._max_frequency

    @max_frequency.setter
    def max_frequency(self, value):
        self._max_frequency = value

    def get_points(self) -> Generator:
        freq = self._min_frequency
        counter = 0
        amount = self._amount_frequency
        if amount > 1:
            amount -= 1
            counter -= 1

        if not self._log:
            delta = (self._max_frequency - self._min_frequency) / amount
        else:
            delta = math.pow(self._max_frequency / self._min_frequency, (1 / amount))

        print(f"delta: {delta}, self._amount_frequency {self._amount_frequency}, amount {amount}, "
              f"max {self._max_frequency}, min {self._min_frequency}")

        while counter < amount:
            yield self._shape, freq, self._amplitude, self._offset
            counter += 1
            if self._log:
                freq *= delta
            else:
                freq += delta

    def point_amount(self) -> int:
        return self._amount_frequency

    def get_config(self) -> Dict:
        return {
            # Fungen vars
            "shape": self._shape,
            "amplitude": self._amplitude,
            "offset": self._offset,
            # Config vars
            "log_scale": self._log,
            "min_frequency": self._min_frequency,
            "max_frequency": self._max_frequency,
            "amount_frequency": self._amount_frequency
        }

    def set_config(self, config: Dict):
        # UI Vars
        self.shape = config["shape"]
        self.amplitude = config["amplitude"]
        self.offset = config["offset"]
        self.log_scale = config["log_scale"]
        self.min_frequency = config["min_frequency"]
        self.max_frequency = config["max_frequency"]
        self.amount_frequency = config["amount_frequency"]

    def variable_documentation(self) -> Dict[str, str]:
        return {

        }


class FunGenConfUi(ConfigurationUI):
    gui = (".", "conf_ui.ui")
    backend: FunGen

    def __init__(self, backend):
        super().__init__(backend=backend)
        connect_feat(self.widget.shape_cb, self.backend, "shape")
        connect_feat(self.widget.amplitude_sb, self.backend, "amplitude")
        connect_feat(self.widget.offset_sb, self.backend, "offset")
        connect_feat(self.widget.log_check, self.backend, "log_scale")
        connect_feat(self.widget.freq_max_sb, self.backend, "max_frequency")
        connect_feat(self.widget.freq_min_sb, self.backend, "min_frequency")
        connect_feat(self.widget.freq_amount_sb, self.backend, "amount_frequency")
