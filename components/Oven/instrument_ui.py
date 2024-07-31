from time import sleep
from typing import Dict, Any, Generator

from SER.interfaces import ConfigurableInstrument, ConfigurationUI
from lantz.core import Feat
from lantz.qt import InstrumentSlot
from lantz.qt.connect import connect_feat
from pyvisa import VisaIOError

from .TMS94 import T94Driver, T94Status


class OvenInstrument(ConfigurableInstrument):
    oven: T94Driver

    def __init__(self, oven):
        self.oven = oven
        super().__init__()
        self.oven.initialize()
        self.temperature = self.oven.temperature()
        self._rate = 0
        self._min_temp = 0
        self._max_temp = 0
        self._point_amount = 1

    def get_config(self) -> Dict:
        return {
            "rate": self._rate,
            "min": self._min_temp,
            "max": self._max_temp,
            "amount": self._point_amount
        } | super().get_config()

    def set_config(self, config: Dict):
        super().set_config(config)
        self.rate = config["rate"]
        self.min_temp = config["min"]
        self.max_temp = config["max"]
        self.temp_amount = config["amount"]

    def configure(self, temp) -> Dict[str, Any]:
        self.oven.limit(temp)
        self.oven.start()
        temp_reached = True
        if self.oven.temperature() < temp:
            temp_reached = False
        while not temp_reached:
            sleep(0.1)
            try:
                if not (self.oven.temperature() < temp and self.oven.status != T94Status.HOLDING_LIMIT
                        and self.oven.status != T94Status.STOPPED):
                    temp_reached = True
            except VisaIOError:
                pass

        return {"Temperature": temp}

    def get_points(self) -> Generator:
        minimum = min(self._max_temp, self._min_temp)
        maximum = max(self._max_temp, self._min_temp)
        if self._point_amount == 1:
            yield tuple([self._max_temp])
        else:
            delta = abs(maximum - minimum) / (self._point_amount - 1)
            current = minimum
            while current <= maximum:
                yield tuple([current])
                current += delta

    def point_amount(self) -> int:
        return self._point_amount

    def variable_documentation(self) -> Dict[str, str]:
        return {
            "Temperature": "The temperature at the moment the measure was taken in degrees celsius"
        }

    @Feat
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = value
        self.oven.rate(value)

    @Feat
    def min_temp(self):
        return self._min_temp

    @min_temp.setter
    def min_temp(self, value):
        self._min_temp = value

    @Feat
    def max_temp(self):
        return self._max_temp

    @max_temp.setter
    def max_temp(self, value):
        self._max_temp = value

    @Feat
    def temp_amount(self):
        return self._point_amount

    @temp_amount.setter
    def temp_amount(self, value):
        self._point_amount = value

    def finalize(self):
        self.stop()

    def stop(self):
        self.oven.stop()


class OvenUI(ConfigurationUI):
    gui = "conf.ui"

    backend: OvenInstrument

    def __init__(self, backend):
        super().__init__(backend=backend)
        backend.initialize()
        connect_feat(self.widget.min_temp_sb, self.backend, "min_temp")
        connect_feat(self.widget.max_temp_sb, self.backend, "max_temp")
        connect_feat(self.widget.rate_temp_sb, self.backend, "rate")
        connect_feat(self.widget.amount_temp_sb, self.backend, "temp_amount")