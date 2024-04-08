import ctypes
import os
import re
import sys
import configparser
import tempfile

from ctypes import byref
from pathlib import Path
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from lantz import Driver, Feat
from lantz.core.log import ERROR, DEBUG, get_logger

from libximc import (lib, EnumerateFlags, controller_name_t, engine_settings_t, Result, status_t, get_position_t,
                     edges_settings_t, feedback_settings_t, EngineFlags, BorderFlags, FeedbackFlags, EnderFlags,
                     FeedbackType, StateFlags, control_settings_t, move_settings_t)

probe_flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
enum_hints = b"addr=192.168.0.1,172.16.2.3"


def get_available_motors() -> dict[str, str]:
    motors = {}
    dev_enum = lib.enumerate_devices(probe_flags, enum_hints)
    dev_count = lib.get_device_count(dev_enum)
    controller_name = controller_name_t()
    for dev_ind in range(0, dev_count):
        enum_name = lib.get_device_name(dev_enum, dev_ind)
        result = lib.get_enumerate_device_controller_name(dev_enum, dev_ind, byref(controller_name))
        if result == Result.Ok:
            motors[str(controller_name.ControllerName)] = enum_name
    return motors


class ClosedMotorException(Exception):
    pass


class MotorStatus:
    def __init__(self, interval, device_id, _lib, virtual: bool):
        self.interval = interval
        self.status = status_t()
        self.running = True
        self.lib = _lib
        self.device_id = device_id
        self.virtual = virtual

    def update_status(self):
        while self.running and not self.virtual:
            result = self.lib.get_status(self.device_id, byref(self.status))
            if result != Result.Ok:
                self.running = False
            if self.status.Flags & StateFlags.STATE_ALARM:
                self.running = False
                self.lib.command_stop(self.device_id)
            sleep(self.interval.total_seconds())


class Motor(Driver):
    x: int
    y: int
    position_margin = 40  # This is how much out of position we are in move_to_sync before we warn
    _device_id = None
    _lib = lib
    _motor: str
    _status: MotorStatus

    # Status interval: this time indicates how long we wait between statuses.
    status_interval = timedelta(milliseconds=10)
    _status_thread: Thread
    position_struct: get_position_t

    def __init__(self):
        super().__init__()
        self.logger_name = 'SER.Driver.' + str(self)
        self.logger = get_logger(self.logger_name)
        self.virtual = False
        self._motor = ""

    def current_motor(self):
        return self._motor

    def open_motor(self, motor, file=None):
        self._motor = motor
        if motor == "virtual":
            self.virtual = True
            path = Path(str(tempfile.gettempdir()) + "/file.bin")
            uri = path.as_uri()
            uri = re.sub(r'^file', 'xi-emu', uri).encode()
            self._device_id = self._lib.open_device(uri)
        else:
            self._device_id = self._lib.open_device(motor)
        if self._device_id == -1:
            self.log(ERROR, "Failed to open Device")
            raise Exception("Failed Opening Device")
        if file:
            self.setup_file(file)
        else:
            self.log(ERROR, "No configuration file")
        self._status = MotorStatus(self.status_interval, self._device_id, self._lib, self.virtual)
        self._status_thread = Thread(target=self._status.update_status)
        self._status_thread.start()

    def close_motor(self):
        self.log_debug(f"Starting Closure motor")
        self._status.running = False
        if hasattr(self, "_device_id") and not self.virtual:
            try:
                device_id = ctypes.c_int()
                device_id.value = self._device_id
                self._lib.close_device(ctypes.byref(device_id))
            except Exception as e:
                self.log_error(f"The motor failed to close with error {e}")
        if hasattr(self, "_status_thread"):
            self._status_thread.join()

    def STOP(self):
        return self._lib.command_stop(self._device_id) == Result.Ok

    def move_to(self, position):
        if self._device_id is None:
            raise ClosedMotorException
        if not self._status.running:
            raise Exception("Motor not running.")
        result = self._lib.command_move(self._device_id, int(position), 0)
        self.log(DEBUG, str(result))

        if self.virtual:
            self._status.status.CurPosition = int(position)
            self._status.status.EncPosition = int(position)
        return Result.Ok == result

    def move_to_sync(self, position, timeout=timedelta(seconds=1)):
        timeout_time = datetime.now() + timeout
        result = self.move_to(position)
        self.log(DEBUG, str(result))
        if not result:
            return False
        if self.virtual:
            return True

        # State machine for checking if we arrived
        # first check, wait for it to be moving. The move command has a delay before we start moving
        while self.stopped() and abs(self.position - position) > self.position_margin:
            sleep(self.status_interval.total_seconds())
            if datetime.now() > timeout_time:
                print("Motor never started moving.")
                return False

        # now that we're moving, wait for it to stop
        while not self.stopped():
            sleep(self.status_interval.total_seconds())
            if datetime.now() > timeout_time:
                print("Motor never stopped moving.")
                return False

        # We return false if for some reason we are at the bad position
        # TODO: Have an if vs encoder
        if abs(self.position - position) > self.position_margin:
            print("We reached the wrong position.")
            return False

        return True

    def stopped(self):
        if self.virtual:
            return True
        if not self._status.running:
            raise Exception("Motor not running.")
        return self._status.status.CurSpeed == 0 and self._status.status.MoveSts == 0

    def zero(self):
        if not self._status.running:
            raise Exception("Motor not running.")
        return self._lib.command_zero(self._device_id) == Result.Ok

    @Feat
    def position(self) -> int:
        """Returns the position of the motor stored internally in counts. Note that it uses the last updated status
        and does not wait for a status refresh"""
        return self._status.status.CurPosition

    @Feat
    def encoder_position(self) -> int:
        """Returns the position of the motor based on the encoder in counts. Note that it uses the last updated status
        and does not wait for a status refresh"""
        return self._status.status.EncPosition

    def _setup_feedback_encoder(self, config):
        feedback_settings = feedback_settings_t()
        result = self._lib.get_feedback_settings(self._device_id, byref(feedback_settings))
        if result != Result.Ok:
            raise Exception("Failed to get feedback settings")
        if "Engine" in config:
            if "Feedback_type" in config["Engine"]:
                if config["Engine"]["Feedback_type"] == "ENCODER":
                    feedback_settings.FeedbackType = FeedbackType.FEEDBACK_ENCODER
                elif config["Engine"]["Feedback_type"] == "NONE":
                    feedback_settings.FeedbackType = FeedbackType.FEEDBACK_NONE
                elif config["Engine"]["Feedback_type"] == "EMF":
                    feedback_settings.FeedbackType = FeedbackType.FEEDBACK_EMF
                else:
                    raise Exception("Unknown Feedback Type")
            if "Encoder_CPT" in config["Engine"]:
                feedback_settings.IPS = int(config["Engine"]["Encoder_CPT"])
                feedback_settings.CountsPerTurn = int(config["Engine"]["Encoder_CPT"])
            flag = 0
            if "Encoder_reverse" in config["Engine"]:
                if "true" == config["Engine"]["Encoder_reverse"]:
                    flag += FeedbackFlags.FEEDBACK_ENC_REVERSE
            if "Feedback_enc_type" in config["Engine"]:
                if config["Engine"]["Feedback_enc_type"] == "SINGLE_ENDED":
                    flag += FeedbackFlags.FEEDBACK_ENC_TYPE_SINGLE_ENDED
                elif config["Engine"]["Feedback_enc_type"] == "DIFFERENTIAL":
                    flag += FeedbackFlags.FEEDBACK_ENC_TYPE_DIFFERENTIAL
                else:
                    pass
            feedback_settings.FeedbackFlags = flag
        result = self._lib.set_feedback_settings(self._device_id, byref(feedback_settings))
        if result != Result.Ok:
            raise Exception("Failed to set feedback settings")
        self._feedback_settings = feedback_settings

    def _setup_borders(self, config):
        edges_settings = edges_settings_t()
        result = self._lib.get_edges_settings(self._device_id, byref(edges_settings))
        if result != Result.Ok:
            raise Exception("Failed to get feedback settings")
        if "Borders" in config:
            border_flags = 0
            if "Border_is_encoder" in config["Borders"]:
                if "true" == config["Borders"]["Border_is_encoder"]:
                    border_flags += BorderFlags.BORDER_IS_ENCODER
            if "Stop_at_left_border" in config["Borders"]:
                if "true" == config["Borders"]["Stop_at_left_border"]:
                    border_flags += BorderFlags.BORDER_STOP_LEFT
            if "Stop_at_right_border" in config["Borders"]:
                if "true" == config["Borders"]["Stop_at_right_border"]:
                    border_flags += BorderFlags.BORDER_STOP_RIGHT
            if "Borders_swap_misset_detection" in config["Borders"]:
                if "true" == config["Borders"]["Borders_swap_misset_detection"]:
                    border_flags += BorderFlags.BORDERS_SWAP_MISSET_DETECTION
            edges_settings.BorderFlags = border_flags

            ender_flags = 0
            if "Limit_switch_ender_swap" in config["Borders"]:
                if "true" == config["Borders"]["Limit_switch_ender_swap"]:
                    ender_flags += EnderFlags.ENDER_SWAP
            if "Limit_switch_1_pushed_is_closed" in config["Borders"]:
                if "true" == config["Borders"]["Limit_switch_1_pushed_is_closed"]:
                    ender_flags += EnderFlags.ENDER_SW1_ACTIVE_LOW
            if "Limit_switch_2_pushed_is_closed" in config["Borders"]:
                if "true" == config["Borders"]["Limit_switch_2_pushed_is_closed"]:
                    ender_flags += EnderFlags.ENDER_SW2_ACTIVE_LOW
            edges_settings.EnderFlags = ender_flags

            if "Left_border" in config["Borders"]:
                edges_settings.LeftBorder = int(config["Borders"]["Left_Border"])
            if "Left_border_usteps" in config["Borders"]:
                edges_settings.uLeftBorder = int(config["Borders"]["Left_border_usteps"])
            if "Right_border" in config["Borders"]:
                edges_settings.RightBorder = int(config["Borders"]["Right_border"])
            if "Right_border_usteps" in config["Borders"]:
                edges_settings.uRightBorder = int(config["Borders"]["Right_border_usteps"])
        result = self._lib.set_edges_settings(self._device_id, byref(edges_settings))
        if result != Result.Ok:
            raise Exception("Failed to set feedback settings")
        self._feedback_settings = edges_settings

    def _setup_engine(self, config):
        engine_settings = engine_settings_t()
        result = self._lib.get_engine_settings(self._device_id, byref(engine_settings))
        if result != Result.Ok:
            raise Exception("Failed to get engine settings")

        if "Engine" in config:
            if "Play_compensation" in config["Engine"]:
                engine_settings.Antiplay = int(config["Engine"]["Play_compensation"])
            if "Microstep_mode" in config["Engine"]:
                engine_settings.MicrostepMode = int(config["Engine"]["Microstep_mode"])
            if "Max_speed_steps" in config["Engine"]:
                engine_settings.NomSpeed = int(config["Engine"]["Max_speed_steps"])
            if "Rated_current" in config["Engine"]:
                engine_settings.NomCurrent = int(config["Engine"]["Rated_current"])
            if "Rated_voltage" in config["Engine"]:
                engine_settings.NomVoltage = int(config["Engine"]["Rated_voltage"])
            if "Steps_per_turn" in config["Engine"]:
                engine_settings.StepsPerReb = int(config["Engine"]["Steps_per_turn"])

            engine_flags = 0
            if "Reverse_enable" in config["Engine"]:
                if "true" == config["Engine"]["Reverse_enable"]:
                    engine_flags += EngineFlags.ENGINE_REVERSE
            if "Current_as_RMS_enable" in config["Engine"]:
                if "true" == config["Engine"]["Current_as_RMS_enable"]:
                    engine_flags += EngineFlags.ENGINE_CURRENT_AS_RMS
            if "Use_max_speed" in config["Engine"]:
                if "true" == config["Engine"]["Reverse_enable"]:
                    engine_flags += EngineFlags.ENGINE_MAX_SPEED
            if "Play_compensation_enable" in config["Engine"]:
                if "true" == config["Engine"]["Play_compensation_enable"]:
                    engine_flags += EngineFlags.ENGINE_ANTIPLAY
            if "Acceleration_enable" in config["Engine"]:
                if "true" == config["Engine"]["Acceleration_enable"]:
                    engine_flags += EngineFlags.ENGINE_ACCEL_ON
            if "Limit_speed_enable" in config["Engine"]:
                if "true" == config["Engine"]["Reverse_enable"]:
                    engine_flags += EngineFlags.ENGINE_LIMIT_RPM
            if "Max_voltage_enable" in config["Engine"]:
                if "true" == config["Engine"]["Max_voltage_enable"]:
                    engine_flags += EngineFlags.ENGINE_LIMIT_VOLT
            if "Max_current_enable" in config["Engine"]:
                if "true" == config["Engine"]["Max_current_enable"]:
                    engine_flags += EngineFlags.ENGINE_LIMIT_CURR

        result = self._lib.set_engine_settings(self._device_id, byref(engine_settings))
        if result != Result.Ok:
            raise Exception("Failed to get engine settings")

    def setup_file(self, file):
        config = configparser.ConfigParser()
        config.read_file(file)
        self._setup_feedback_encoder(config)
        self._setup_borders(config)
        self._setup_engine(config)
        return config

    def get_engine_settings(self) -> engine_settings_t:
        engine_settings = engine_settings_t()
        result = self._lib.get_engine_settings(self._device_id, byref(engine_settings))
        if result != Result.Ok:
            pass  # We should do something here
        return engine_settings

    def set_engine_settings(self, engine_settings: engine_settings_t) -> Result:
        return self._lib.get_engine_settings(self._device_id, byref(engine_settings))

    def get_control_settings(self) -> control_settings_t:
        control_settings = control_settings_t()
        result = self._lib.get_control_settings(self._device_id, byref(control_settings))
        if result != Result.Ok:
            pass  # We should do something here
        return control_settings

    def get_move_settings(self) -> move_settings_t:
        move_settings = move_settings_t()
        result = self._lib.get_move_settings(self._device_id, byref(move_settings))
        if result != Result.Ok:
            pass  # We should do something here
        return move_settings

    def set_move_settings(self, move_settings: move_settings_t) -> Result:
        return self._lib.set_move_settings(self._device_id, byref(move_settings))

    @Feat
    def antiplay_enabled(self):
        return self.get_engine_settings().EngineFlags & EngineFlags.ENGINE_ANTIPLAY

    @antiplay_enabled.setter
    def antiplay_enabled(self, value):
        engine_settings = self.get_engine_settings()
        if value:
            engine_settings.EngineFlags |= EngineFlags.ENGINE_ANTIPLAY
        else:
            engine_settings.EngineFlags ^= ~EngineFlags.ENGINE_ANTIPLAY
        self.set_engine_settings(engine_settings)

    @Feat
    def antiplay_steps(self):
        return self.get_engine_settings().Antiplay

    @antiplay_steps.setter
    def antiplay_steps(self, value):
        engine_settings = self.get_engine_settings()
        engine_settings.Antiplay = value
        self.set_engine_settings(engine_settings)

    @Feat
    def speed(self):
        return self.get_move_settings().Speed

    @speed.setter
    def speed(self, value):
        move_settings = self.get_move_settings()
        move_settings.Speed = value
        self.set_move_settings(move_settings)

    @Feat
    def accel(self):
        return self.get_move_settings().Accel

    @accel.setter
    def accel(self, value):
        move_settings = self.get_move_settings()
        move_settings.Accel = value
        self.set_move_settings(move_settings)

    @Feat
    def decel(self):
        return self.get_move_settings().Decel

    @decel.setter
    def decel(self, value):
        move_settings = self.get_move_settings()
        move_settings.Decel = value
        self.set_move_settings(move_settings)

    @Feat
    def antiplay_speed(self):
        return self.get_move_settings().AntiplaySpeed

    @antiplay_speed.setter
    def antiplay_speed(self, value):
        move_settings = self.get_move_settings()
        move_settings.AntiplaySpeed = value
        self.set_move_settings(move_settings)
