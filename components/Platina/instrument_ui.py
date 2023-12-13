from typing import Dict, Generator, Any

from SER.interfaces import ConfigurationUI, ConfigurableInstrument
from lantz import Feat
from lantz.qt.connect import connect_feat


class Platina(ConfigurableInstrument):

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self._min = 0
        self._max = 1
        self._amount = 2

    @Feat
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self._min = value

    @Feat
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value

    @Feat
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    def configure(self, *args) -> Dict[str, Any]:
        pass

    def get_points(self) -> Generator:
        pass

    def point_amount(self) -> int:
        pass

    def variable_documentation(self) -> Dict[str, str]:
        pass


class LockinUI(ConfigurationUI):
    gui = "conf.ui"

    backend: Platina

    def __init__(self, backend):
        super().__init__(backend=backend)
        backend.initialize()
        connect_feat(self.widget.time_constant_cb, self.backend.lockin, "time_constants")
        connect_feat(self.widget.input_gain_cb, self.backend.lockin, "sensitivity")
        connect_feat(self.widget.slope_cb, self.backend.lockin, "lockin_roll_off")
