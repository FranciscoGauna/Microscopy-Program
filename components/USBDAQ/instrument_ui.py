import math
import random
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from os import path
from threading import Thread
from time import sleep
from typing import Dict, Generator, Any

from PyQt5 import uic
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QLabel, QCheckBox, QDialog, QVBoxLayout
from SER.interfaces import ObservableInstrument, ConfigurationUI
from keyboard import is_pressed
from lantz import Feat
from lantz.qt.connect import connect_feat
from mcculw.enums import DigitalPortType, DigitalIODirection

from .USB2527 import USB2527
from ..LinePlotter import LinePlotter


class DACInstrument(ObservableInstrument):
    """
    Note: this instrument is highly connected to the specific configuration of the devices in the specific laboratory
    """

    def __init__(self, DAC: USB2527, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self.dac = DAC
        self.checking_focus = False
        self.status = DACStatus(DAC)

        self._focus_value = 0
        self._focus_threshold = 0
        self._motor_speed = 1
        self._min_sum = 0.01
        self._offset_sum = 0
        self._offset_fe = 0
        self._check_focus = False
        self._laser_potency = 99
        self._laser_on = False
        self.initialized = False

        self.currently_moving = False
        self.checking_focus = False

        self.dac.configure_digital_port(DigitalPortType.FIRSTPORTA, DigitalIODirection.OUT)

    def initialize(self, register_finalizer=False):
        self.initialized = True
        super().initialize(register_finalizer)

    @Feat
    def focus_value(self):
        return self._focus_value

    @focus_value.setter
    def focus_value(self, value):
        self._focus_value = value

    @Feat
    def focus_threshold(self):
        return self._focus_threshold

    @focus_threshold.setter
    def focus_threshold(self, value):
        self._focus_threshold = value

    @Feat
    def motor_speed(self):
        return self._motor_speed

    @motor_speed.setter
    def motor_speed(self, value):
        self._motor_speed = value

    @Feat
    def min_sum(self):
        return self._min_sum

    @min_sum.setter
    def min_sum(self, value):
        self._min_sum = value

    @Feat
    def offset_sum(self):
        return self._offset_sum

    @offset_sum.setter
    def offset_sum(self, value):
        self._offset_sum = value

    @Feat
    def offset_fe(self):
        return self._offset_fe

    @offset_fe.setter
    def offset_fe(self, value):
        self._offset_fe = value

    @Feat
    def check_focus(self):
        return self._check_focus

    @check_focus.setter
    def check_focus(self, value):
        self._check_focus = value

    @Feat
    def laser_potency(self):
        return self._laser_potency

    @laser_potency.setter
    def laser_potency(self, value):
        self._laser_potency = value
        self.update_laser()

    @Feat
    def laser_on(self):
        return self._laser_on

    @laser_on.setter
    def laser_on(self, value):
        self._laser_on = value
        self.update_laser()

    def update_laser(self):
        if self._laser_on:
            divisor = (self._laser_potency / 100)
            self.dac.write_analog_input(2, 3.2 * divisor)
        else:
            self.dac.write_analog_input(2, 0)

    def focus(self) -> bool:
        if not self._check_focus:
            return True

        abcd_sum = self.status.abcd_sum
        focus_error = self.status.focus_error

        if abcd_sum < self._min_sum:
            return False
        return abs((focus_error / abcd_sum) - self._focus_value) < self._focus_threshold

    def check_if_should_run(self, timeout=10):
        end_time = datetime.now() + timedelta(seconds=timeout)
        while self.checking_focus:
            if self.focus() or self.status.abcd_sum < self._min_sum:
                self.checking_focus = False
            if datetime.now() > end_time:
                self.checking_focus = False
            sleep(0.05)

    def focus_sync(self) -> bool:
        if self._check_focus is False:
            return True
        if self.focus():
            return True

        self.checking_focus = True
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(DACInstrument.check_if_should_run, self)
            # Enable
            # Set sens
            # Move
            while self.checking_focus:
                pass
            # Disable
        return self.focus()

    def variable_documentation(self) -> Dict[str, str]:
        return {
            "Probe Reflectance": "The reflectance given by the gas",
            "Sum": "The sum of the 4 corners ABCD",
            "Focus Error": "The difference between the corners (A+B)-(C+D)",
        }

    def get_config(self) -> Dict:
        return {
            "laser_on": self.laser_on,
            "check_focus": self.check_focus,
            "focus_value": self.focus_value,
            "focus_threshold": self.focus_threshold,
            "motor_speed": self.motor_speed,
            "min_sum": self.min_sum,
            "offset_sum": self.offset_sum,
            "offset_fe": self.offset_fe,
        }

    def set_config(self, config: Dict):
        self.laser_on = config["laser_on"]
        self.check_focus = config["check_focus"]
        self.focus_value = config["focus_value"]
        self.focus_threshold = config["focus_threshold"]
        self.motor_speed = config["motor_speed"]
        self.min_sum = config["min_sum"]
        self.offset_sum = config["offset_sum"]
        self.offset_fe = config["offset_fe"]

    def observe(self, *args) -> Dict[str, Any]:
        return {
            "Probe Reflectance": self.status.probe_reflectance,
            "Sum": self.status.abcd_sum,
            "Focus Error": self.status.focus_error,
        }

    def sens(self, sens: bool):
        self.dac.write_digital_input(DigitalPortType.FIRSTPORTA, 1, sens)

    def move(self, time=0.1):
        if self.currently_moving:
            return
        self.currently_moving = True
        self.dac.write_digital_input(DigitalPortType.FIRSTPORTA, 2, True)
        steps = math.trunc(time * self._motor_speed)
        step_timer = 0.5 / self._motor_speed
        for i in range(steps):
            self.dac.write_digital_input(DigitalPortType.FIRSTPORTA, 0, False)
            sleep(step_timer)
            self.dac.write_digital_input(DigitalPortType.FIRSTPORTA, 0, True)
            sleep(step_timer)
        self.dac.write_digital_input(DigitalPortType.FIRSTPORTA, 2, False)
        self.currently_moving = False

    def stop(self):
        self.status.running = False
        self.status.thread.join()


class DACStatus:
    abcd_sum: float
    probe_reflectance: float
    focus_error: float
    a: float
    b: float
    c: float
    d: float

    def __init__(self, dac: USB2527):
        self.running = True
        self.dac = dac
        self.read_status()
        self.thread = Thread(target=self.update_status)
        self.thread.start()

    def update_status(self):
        while self.running:
            self.read_status()
            sleep(0.01)

    def read_status(self):
        self.abcd_sum = self.dac.read_analog_input(0)
        self.probe_reflectance = self.dac.read_analog_input(2)
        self.a = self.dac.read_analog_input(7)
        self.b = self.dac.read_analog_input(6)
        self.c = self.dac.read_analog_input(5)
        self.d = self.dac.read_analog_input(4)
        self.focus_error = (self.a + self.c) - (self.b + self.d)


class DACGraphs(QDialog):
    error_focus_graph: LinePlotter
    sum_graph: LinePlotter
    reflectance_graph: LinePlotter
    error_focus_layout: QVBoxLayout
    sum_layout: QVBoxLayout
    reflectance_layout: QVBoxLayout

    def __init__(self):
        super().__init__()
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "graphs.ui")
        uic.loadUi(ui_file_path, self)

        self.error_focus_graph = LinePlotter(("timestamp", "time", "Time"),
                                             ("dac", "focus_error", "Suma"), max_points=500)
        self.sum_graph = LinePlotter(("timestamp", "time", "Time"),
                                     ("dac", "abcd_sum", "Reflectancia"), max_points=500)
        self.reflectance_graph = LinePlotter(("timestamp", "time", "Time"),
                                             ("dac", "probe_reflectance", "Error de Foco"), max_points=500, scatter=False)
        self.error_focus_layout.addWidget(self.error_focus_graph)
        self.sum_layout.addWidget(self.sum_graph)
        self.reflectance_layout.addWidget(self.reflectance_graph)
        self.time = datetime.now()

    def update_with_data(self, focus_error, abcd_sum, probe_reflectance):
        data = [{
            "timestamp": {"time": (datetime.now() - self.time).total_seconds()},
            "dac": {
                "focus_error": focus_error,
                "abcd_sum": abcd_sum,
                "probe_reflectance": probe_reflectance
            }
        }]
        self.error_focus_graph.add_data(data)
        self.sum_graph.add_data(data)
        self.reflectance_graph.add_data(data)


class DACUI(ConfigurationUI):
    gui = "conf.ui"
    backend: DACInstrument

    def __init__(self, backend, move_left_key="K", move_right_key="L"):
        super().__init__(backend=backend)

        self.move_left_key = move_left_key
        self.move_right_key = move_right_key

        connect_feat(self.widget.laser_potency_slider, self.backend, "laser_potency")
        connect_feat(self.widget.laser_on_cb, self.backend, "laser_on")
        connect_feat(self.widget.focus_control_cb, self.backend, "check_focus")
        connect_feat(self.widget.z_focus_sb, self.backend, "focus_value")
        connect_feat(self.widget.range_focus_sb, self.backend, "focus_threshold")
        connect_feat(self.widget.motor_speed_sb, self.backend, "motor_speed")
        connect_feat(self.widget.sum_min_sb, self.backend, "min_sum")
        connect_feat(self.widget.sum_offset_sb, self.backend, "offset_sum")
        connect_feat(self.widget.fe_offset_sb, self.backend, "offset_fe")
        self.widget.focus_display_cb.setEnabled(False)
        self.widget.set_range_bt.pressed.connect(self.set_focus)
        self.widget.graphs_bt.pressed.connect(self.show_graphs)
        self.graphs = DACGraphs()

        self.timer = QTimer()
        self.timer.setInterval(100)  # TODO: remove magic number
        self.timer.setTimerType(Qt.CoarseTimer)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start()

    def update_gui(self):
        if self.backend.initialized:
            self.timer.stop()
            return
        self.widget.laser_potency_lb.setText(f"Potencia laser ({self.backend.laser_potency}%)")
        if self.widget.focus_display_cb.isChecked() != self.backend.focus():
            self.widget.focus_display_cb.toggle()
        self.graphs.update_with_data(
            self.backend.status.focus_error,
            self.backend.status.abcd_sum,
            self.backend.status.probe_reflectance,
        )
        if is_pressed(self.move_left_key) != is_pressed(self.move_right_key):
            self.backend.sens(is_pressed(self.move_left_key))
            self.backend.move(1)

    def set_focus(self):
        value = 0
        try:
            value = self.backend.status.focus_error / self.backend.status.abcd_sum
        except ZeroDivisionError:
            pass
        self.backend.focus_value = value

    def show_graphs(self):
        self.graphs.show()