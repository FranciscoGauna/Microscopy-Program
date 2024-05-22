from datetime import datetime
from time import sleep
from typing import Dict, Generator, Any

from keyboard import is_pressed
from PyQt5.QtCore import QTimer, Qt
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
        if not self.motor.move_to_sync(position):
            self.log_error(f"We failed to move to position: {position}!")
        return {
            "position": position,
            "enc_position": self.motor.encoder_position,
            "motor_position": self.motor.position
        }

    def get_points(self) -> Generator:
        delta = (self._final_point - self._initial_point) / self._amount
        for i in range(self._amount):
            yield tuple([self._initial_point + i * delta])

    def point_amount(self) -> int:
        return self._amount

    def variable_documentation(self) -> Dict[str, str]:
        # ENCODER: if we adapt it to a motor without encoder we need to change this text
        return {
            "position": "The position sent to the motor. With the encoder, that position should always be accurate",
            "motor_position": "The position that the motor is reporting internally after completing the move.",
            "enc_position": "The position that the encoder is reporting internally after completing the move."
        }

    def stop(self):
        self.motor.STOP()
        self.motor.close_motor()

    def get_config(self) -> Dict:
        return {
            "amount": self._amount,
            "final_point": self._final_point,
            "initial_point": self._initial_point,
            "antiplay_enabled": self.motor.antiplay_enabled,
            "antiplay_steps": self.motor.antiplay_steps,
            "antiplay_speed": self.motor.antiplay_speed,
            "speed": self.motor.speed,
            "accel": self.motor.accel,
            "decel": self.motor.decel,
        } | super().get_config()

    def set_config(self, config: Dict):
        super().set_config(config)
        self.amount = config["amount"]
        self._final_point = config["final_point"]
        self._initial_point = config["initial_point"]
        self.motor.antiplay_enabled = bool(config["initial_point"])
        self.motor.antiplay_steps = int(config["initial_point"])
        self.motor.antiplay_speed = int(config["initial_point"])
        self.motor.speed = int(config["speed"])
        self.motor.accel = int(config["accel"])
        self.motor.decel = int(config["decel"])


class PlatinaUI(ConfigurationUI):
    gui = "conf.ui"

    backend: Platina
    timer: QTimer

    def __init__(self, backend, move_left_key="left", move_right_key="right"):
        super().__init__(backend=backend)
        connect_feat(self.widget.initial_pos_sb, self.backend, "initial_point")
        connect_feat(self.widget.final_pos_sb, self.backend, "final_point")
        connect_feat(self.widget.amount_pos_sb, self.backend, "amount")
        connect_feat(self.widget.backlash_cb, self.backend.motor, "antiplay_enabled")
        connect_feat(self.widget.antiplay_sb, self.backend.motor, "antiplay_steps")
        connect_feat(self.widget.speed_sb, self.backend.motor, "speed")
        connect_feat(self.widget.acceleration_sb, self.backend.motor, "accel")
        connect_feat(self.widget.deceleration_sb, self.backend.motor, "decel")
        connect_feat(self.widget.antiplay_speed_sb, self.backend.motor, "antiplay_speed")
        self.widget.zero_button.pressed.connect(self.backend.zero)

        # TODO: remember to change this to the localization
        self.widget.pos_label.setText(f"Posicion Actual ({self.backend.conversion_units}):")

        self.move_left_key = move_left_key
        self.move_right_key = move_right_key

        self.timer = QTimer()
        self.timer.setInterval(100)  # TODO: remove magic number
        self.timer.setTimerType(Qt.CoarseTimer)
        self.timer.timeout.connect(self.key_pressed)
        self.timer.start()

    def key_pressed(self):
        if not self.backend.initialized:  # We don't want this to move the motor during the experiment run
            # Hack, we shouldn't be forcing an update here of the gui
            self.widget.pos_number.display(self.backend.position())
            if is_pressed(self.move_left_key) != is_pressed(self.move_right_key):
                pos = self.backend.motor.encoder_position  # ENCODER: check if it's encoder feedback
                if is_pressed(self.move_left_key):
                    pos -= 50  # TODO: rethink how we put this in a way that makes sense
                if is_pressed(self.move_right_key):
                    pos += 50
                self.backend.motor.move_to(pos)
