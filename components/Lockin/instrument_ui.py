import threading
from datetime import datetime
from os import path
from time import sleep
from typing import Dict, Any

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from SER.interfaces import ObservableInstrument, ConfigurationUI
from lantz.qt import InstrumentSlot
from lantz.qt.connect import connect_feat
from pint import get_application_registry

from .anfatec_driver import AnfatecAMU24
from ..BarPlotter import BarPlotter
from ..LinePlotter import LinePlotter

ureg = get_application_registry()
Quantity = ureg.Quantity


class Lockin(ObservableInstrument):
    lockin: AnfatecAMU24 = InstrumentSlot()
    initialized = False

    def initialize(self, register_finalizer=False, is_experiment=True):
        self.initialized = is_experiment
        self.lockin.initialize()

    def observe(self) -> Dict[str, Any]:
        tc_time = Quantity(self.lockin.time_constants).to("s").magnitude
        sleep(tc_time * 100)
        return {
            "amplitude": self.lockin.amplitude.magnitude,
            "phase": self.lockin.phase.magnitude
        }

    def get_config(self) -> Dict:
        """This function returns a dictionary of the values used for the configuration of the lockin. If you want to
         load a new instance with these setting you should add this dictionary to the kwargs when you instantiante the
         class"""
        settings = {
            "reference_on": self.lockin.reference_on,
            "time_constant": self.lockin.time_constants,
            "filter_slope": self.lockin.filter_slope,
            "sensitivity": self.lockin.sensitivity,
            "harmonic": self.lockin.harmonic,
            "coupling": self.lockin.coupling,
            "reference_phase": self.lockin.reference_phase.magnitude,
            "reference_amplitude": self.lockin.reference_amplitude.magnitude,
            "reference_frequency": self.lockin.reference_frequency.magnitude,
        }

        return settings

    def set_config(self, config: Dict):
        self.lockin.reference_on = config["reference_on"]
        self.lockin.time_constants = config["time_constant"]
        self.lockin.filter_slope = config["filter_slope"]
        self.lockin.sensitivity = config["sensitivity"]
        self.lockin.harmonic = config["harmonic"]
        self.lockin.coupling = config["coupling"]
        self.lockin.reference_phase = config["reference_phase"]
        self.lockin.reference_amplitude = config["reference_amplitude"]
        self.lockin.reference_frequency = config["reference_frequency"]

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

    def __init__(self, backend: Lockin):
        super().__init__(backend=backend)
        backend.initialize(is_experiment=False)
        connect_feat(self.widget.time_constant_cb, self.backend.lockin, "time_constants")
        connect_feat(self.widget.input_gain_cb, self.backend.lockin, "sensitivity")
        connect_feat(self.widget.slope_cb, self.backend.lockin, "filter_slope")
        connect_feat(self.widget.harmonic_sb, self.backend.lockin, "harmonic")
        connect_feat(self.widget.pll_check, self.backend.lockin, "reference_on")

        self.dialog = LockinGraphs(backend)
        self.widget.graphs_bt.pressed.connect(self.dialog.show)

    def close_graphs(self):
        self.dialog.close_graphs()


class LockinGraphs(QDialog):
    amplitude_graph: LinePlotter
    phase_graph: BarPlotter
    amplitude_layout: QVBoxLayout
    phase_layout: QVBoxLayout

    def __init__(self, lockin: Lockin):
        super().__init__()
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "graphs.ui")
        uic.loadUi(ui_file_path, self)

        self.amplitude_graph = LinePlotter(("timestamp", "time", "Time"),
                                           ("lockin", "amplitude", "Amplitude"), max_points=500)
        self.phase_graph = BarPlotter(("timestamp", "time", "Time"),
                                      ("lockin", "phase", "Phase"), max_points=500, histogram=True)
        self.amplitude_layout.addWidget(self.amplitude_graph)
        self.phase_layout.addWidget(self.phase_graph)
        self.lockin = lockin
        self.time = datetime.now()
        self.running = True
        self.timer = threading.Thread(target=self.update_with_data)
        self.timer.start()

    def close_graphs(self):
        self.running = False
        self.timer.join()

    def update_with_data(self):
        while not self.lockin.initialized and self.running:
            data = [{
                "timestamp": {"time": (datetime.now() - self.time).total_seconds()},
                "lockin": {
                    "amplitude": self.lockin.lockin.amplitude.magnitude,
                    "phase": self.lockin.lockin.phase.magnitude
                }
            }]
            self.amplitude_graph.add_data(data)
            self.phase_graph.add_data(data)
            sleep(0.1)
