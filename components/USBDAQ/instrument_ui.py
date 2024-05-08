from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep
from typing import Dict, Generator, Any

from SER.interfaces import ObservableInstrument, ConfigurationUI

from .USB2527 import USB2527


class DACInstrument(ObservableInstrument):
    """
    Note: this instrument is highly connected to the specific configuration of the devices in the specific laboratory
    """

    def __init__(self, DAC: USB2527, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self.dac = DAC
        self.checking_focus = False
        self.status = DACStatus(DAC)

    def focus(self) -> bool:
        abcd_sum = self.status.abcd_sum
        focus_error = self.status.focus_error

        return abs(focus_error / abcd_sum) < self.focus_threshold

    def check_if_should_run(self):
        while self.checking_focus:
            if self.focus() or self.status.abcd_sum < self.min_sum:  # TODO: add a timeout?
                self.checking_focus = False
            sleep(0.05)

    def focus_sync(self) -> bool:
        if self.check_focus is False:
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
        return {}

    def set_config(self, config: Dict):
        pass

    def observe(self, *args) -> Dict[str, Any]:
        return {
            "Probe Reflectance": self.status.probe_reflectance,
            "Sum": self.status.abcd_sum,
            "Focus Error": self.status.focus_error,
        }

    def stop(self):
        self.status.running = False
        self.status.thread.join()


class DACStatus:
    abcd_sum: float
    probe_reflectance: float
    focus_error: float

    def __init__(self, dac: USB2527):
        self.running = True
        self.dac = dac
        self.thread = Thread(target=self.update_status)
        self.thread.start()

    def update_status(self):
        while self.running:
            self.abcd_sum = self.dac.read_analog_input(0)
            self.probe_reflectance = self.dac.read_analog_input(2)
            self.focus_error = self.dac.read_analog_input(3)
            sleep(0.01)


class DACUI(ConfigurationUI):
    gui = "conf.ui"

    def __init__(self, backend):
        super().__init__(backend=backend)
        self.widget.graphs_bt.pressed.connect()
