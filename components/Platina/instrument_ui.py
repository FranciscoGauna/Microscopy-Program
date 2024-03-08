from datetime import datetime
from time import sleep
from typing import Dict, Generator, Any

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QCloseEvent
from SER.interfaces import ConfigurationUI, ConfigurableInstrument
from lantz import Feat
from lantz.qt import InstrumentSlot
from lantz.qt.connect import connect_feat

from .motor import Motor


class Platina(ConfigurableInstrument):
    motor: Motor = InstrumentSlot()
    conversion_units: str
    conversion_factor: float

    def __init__(self, **instruments_and_backends):
        filename = instruments_and_backends.pop("filename")
        super().__init__(**instruments_and_backends)
        self._initial_point = 0
        self._final_point = 1
        self._amount = 2
        self.initialized = False

        if filename is not None:
            with open(filename, "r+") as file:
                config = self.motor.setup_file(file)
            self.conversion_units = config["Stage"]["Units"]
            self.conversion_factor = float(config["Stage"]["Lead_screw_pitch"])
            self.conversion_factor /= int(config["Engine"]["Encoder_CPT"])
        else:
            self.conversion_units = "counts"
            self.conversion_factor = 1.0

    def initialize(self, register_finalizer=False):
        super().initialize(register_finalizer)
        self.initialized = True

    def zero(self):
        # ENCODER
        self.motor.zero()

    @Feat
    def position(self) -> float:
        # ENCODER: We use the encoder position here, we are assuming we have an encoder motor
        # TODO: rethink if we need to change this to an option based on the config file
        return self.motor.encoder_position * self.conversion_factor

    @Feat
    def initial_point(self):
        return self._initial_point * self.conversion_factor

    @initial_point.setter
    def initial_point(self, value):
        self._initial_point = value / self.conversion_factor

    @Feat
    def final_point(self):
        return self._final_point * self.conversion_factor

    @final_point.setter
    def final_point(self, value):
        self._final_point = value / self.conversion_factor

    @Feat
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    def configure(self, position) -> Dict[str, Any]:
        # ENCODER: if we adapt it to a motor without encoder feedback we need to add a result indicating the value
        # of the encoder
        print(f"Received motor point: {position}")
        self.motor.move_to_sync(position)
        sleep(0.1)
        return {"position": position}

    def get_points(self) -> Generator:
        delta = (self._final_point - self._initial_point) / self._amount
        for i in range(self._amount):
            print(f"given motor point: {self._initial_point + i * delta}")
            yield tuple([self._initial_point + i * delta])

    def point_amount(self) -> int:
        return self._amount

    def variable_documentation(self) -> Dict[str, str]:
        # ENCODER: if we adapt it to a motor without encoder we need to change this text
        return {"position": "The position sent to the motor. With the encoder, that position should always be accurate"}

    def get_config(self) -> Dict:
        return {
            "amount": self._amount,
            "final_point": self._final_point,
            "initial_point": self._initial_point
        }

    def set_config(self, config: Dict):
        self._amount = config["amount"]
        self._final_point = config["final_point"]
        self._initial_point = config["initial_point"]


class PlatinaUI(ConfigurationUI):
    gui = "conf.ui"

    backend: Platina
    timer: QTimer

    def __init__(self, backend):
        super().__init__(backend=backend)
        backend.initialize()
        connect_feat(self.widget.initial_pos_sb, self.backend, "initial_point")
        connect_feat(self.widget.final_pos_sb, self.backend, "final_point")
        connect_feat(self.widget.amount_pos_sb, self.backend, "amount")
        connect_feat(self.widget.pos_number, self.backend, "position")
        self.widget.zero_button.pressed.connect(self.backend.zero)
        self.timer = QTimer()
        self.timer.setInterval(100)  # TODO: remove magic number
        self.timer.setTimerType(Qt.CoarseTimer)
        self.timer.timeout.connect(self.key_pressed)

    def key_pressed(self):
        if not self.backend.initialized:  # We don't want this to move the motor during the experiment run
            print(f"{datetime.now()}: key_pressed")