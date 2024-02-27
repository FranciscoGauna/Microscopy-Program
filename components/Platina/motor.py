import os
import re
import sys
import configparser

from ctypes import byref
from pathlib import Path
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from lantz import Driver, Feat
from lantz.core.log import ERROR, DEBUG

from libximc import (lib, EnumerateFlags, controller_name_t, engine_settings_t, Result, status_t, get_position_t,
                     edges_settings_t, feedback_settings_t, EngineFlags, BorderFlags, FeedbackFlags, EnderFlags,
                     FeedbackType, StateFlags)

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


class Motor(Driver):
    x: int
    y: int
    virtual = False
    _device_id = None
    _lib = lib
    _motor: str
    _status: status_t
    _status_time = datetime.now()
    _status_interval = timedelta(milliseconds=100)
    _status_thread: Thread
    position_struct: get_position_t

    def __init__(self):
        super().__init__()
        self._motor = ""
        self._status_running = True

    def __del__(self):
        self.close_motor()

    def current_motor(self):
        return self._motor

    def open_motor(self, motor, file=None):
        self._motor = motor
        if motor == "virtual":
            self.virtual = True
            path = Path(str(Path.cwd()) + "/tmp/file.bin")
            uri = path.as_uri()
            uri = re.sub(r'^file', 'xi-emu', uri).encode()
            self._device_id = self._lib.open_device(uri)
        else:
            self._device_id = self._lib.open_device(motor)
        if self._device_id == -1:
            self.log(ERROR, "Failed to open Device")
            raise Exception("Failed Opening Device")
        if file:
            self._setup_file(file)
        else:
            self.log(ERROR, "No configuration file")
        self._status = status_t()
        self._status_running = True
        self._status_thread = Thread(target=self._update_status)
        self._status_thread.start()

    def close_motor(self):
        self.log_debug(f"Starting Closure motor")
        self._status_running = False
        if hasattr(self, "_device_id") and self._device_id != 1:
            self._lib.close_device(self._device_id)
        if hasattr(self, "_status_thread"):
            self._status_thread.join()


    def _update_status(self):
        while self._status_running:
            result = self._lib.get_status(self._device_id, byref(self._status))
            if result != Result.Ok:
                raise Exception("Failed Getting Status")
            if self._status.Flags & StateFlags.STATE_ALARM:
                raise Exception("Motor Alarm!")
            sleep(self._status_interval.seconds)
        self.log_debug(f"Stopping updated")

    def move_to(self, x_count):
        if self._device_id is None:
            raise ClosedMotorException
        result = self._lib.command_move(self._device_id, int(x_count), 0)
        self.log(DEBUG, str(result))
        self._status_time = datetime.now()
        return Result.Ok == result

    def stopped(self):
        if self._motor == "virtual":
            return True
        self._update_status()
        return self._status.CurSpeed == 0 and (self._status.MoveSts % 2) == 0

    @Feat
    def position(self):
        if (datetime.now() - self._status_time) < self._status_interval and hasattr(self, "position_struct"):
            return self.position_struct.Position
        self.position_struct = get_position_t()
        result = self._lib.get_position(self._device_id, byref(self.position_struct))
        self._status_time = datetime.now()
        if result != Result.Ok:
            raise Exception("Failed Getting Status")
        return self.position_struct.Position

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
                    flag += 1
            if "Feedback_enc_type" in config["Engine"]:
                if config["Engine"]["Feedback_enc_type"] == "AUTO":
                    flag = FeedbackFlags.FEEDBACK_ENC_TYPE_AUTO
                elif config["Engine"]["Feedback_enc_type"] == "SINGLE_ENDED":
                    flag += FeedbackFlags.FEEDBACK_ENC_TYPE_SINGLE_ENDED
                elif config["Engine"]["Feedback_enc_type"] == "DIFFERENTIAL":
                    flag += FeedbackFlags.FEEDBACK_ENC_TYPE_DIFFERENTIAL
                else:
                    raise Exception("Unknown Feedback Encoder Type")
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

    def _setup_file(self, file):
        config = configparser.ConfigParser()
        config.read_file(file)
        self._setup_feedback_encoder(config)
        self._setup_borders(config)
        self._setup_engine(config)

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
