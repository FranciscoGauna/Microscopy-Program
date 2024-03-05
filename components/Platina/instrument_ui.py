from typing import Dict, Generator, Any

from PyQt5.QtGui import QCloseEvent
from SER.interfaces import ConfigurationUI, ConfigurableInstrument
from lantz import Feat
from lantz.qt import InstrumentSlot
from lantz.qt.connect import connect_feat

from .motor import Motor


class Platina(ConfigurableInstrument):
    motor: Motor
    conversion_units: str
    conversion_factor: float

    def __init__(self, **instruments_and_backends):
        filename = instruments_and_backends.pop("filename")
        self.motor = instruments_and_backends.pop("motor")
        super().__init__(**instruments_and_backends)
        self._min = 0
        self._max = 1
        self._amount = 2

        if filename is not None:
            with open(filename, "r+") as file:
                config = self.motor.setup_file(file)
            self.conversion_units = config["Stage"]["Units"]
            self.conversion_factor = float(config["Stage"]["Lead_screw_pitch"])
            self.conversion_factor /= int(config["Engine"]["Encoder_CPT"])
        else:
            self.conversion_units = "counts"
            self.conversion_factor = 1.0

    def zero(self):
        # ENCODER
        self.motor.zero()

    @Feat
    def position(self) -> float:
        # ENCODER: We use the encoder position here, we are assuming we have an encoder motor
        # TODO: rethink if we need to change this to an option based on the config file
        return self.motor.encoder_position * self.conversion_factor

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


class PlatinaUI(ConfigurationUI):
    gui = "conf.ui"

    backend: Platina

    def __init__(self, backend):
        super().__init__(backend=backend)
        backend.initialize()
        connect_feat(self.widget.initial_pos_sb, self.backend, "min")
        connect_feat(self.widget.final_pos_sb, self.backend, "max")
        connect_feat(self.widget.amount_pos_sb, self.backend, "amount")
        connect_feat(self.widget.pos_number, self.backend, "position")

