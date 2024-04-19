from enum import Enum
from time import sleep

from lantz import MessageBasedDriver
from pyvisa.constants import StopBits, Parity


class T94Status(Enum):
    STOPPED = 1
    HEATING = 16
    COOLING = 32
    HOLDING_LIMIT = 48
    HOLDING_TIME = 64
    HOLDING_CURRENT = 80


class T94Driver(MessageBasedDriver):
    status = 1
    _rate = 0
    _limit = 0

    @classmethod
    def via_serial(cls, port, name=None, **kwargs):
        return super().via_serial(port, name=name, baud_rate=19200, data_bits=8, stop_bits=StopBits.one,
                                  parity=Parity.none, write_termination="\r", read_termination="\r")

    def query_raw(self, message, length):
        self.resource.write(message)
        sleep(0.01)
        return self.resource.read_raw(length)

    def temperature(self):
        """Returns the current temperature. It also updates the status. Locks for 10 ms to let the buffer update."""
        response = self.query_raw("T", 11)
        self.status = response[0]
        error = response[1]
        # pump = response[2]
        # gen = response[3]
        temp = response[6:10]
        if error != 128:
            self.stop()
            raise Exception(f"Error code {error}")
        return int(temp.decode("ascii"), 16) * 0.1

    def rate(self, value):
        """Rate value in C°/min. Must be between 0 and 200"""
        if value <= 0 <= 200:
            self.stop()
            raise Exception(f"Temperature rate must be between 0 and 200.")
        self.query_raw(f"R1{int(value * 100)}", 1)

    def limit(self, value):
        """Maximum Temperature in C°. Must be between 0 and 1500"""
        self.query_raw(f"L1{int(value * 10)}", 1)

    def start(self):
        """Starts the heating operation."""
        self.query_raw("S", 1)

    def stop(self):
        """Halts the current operation."""
        self.query_raw("E", 1)


class VirtualOven(T94Driver):
    status = T94Status.HOLDING_LIMIT
    _temperature = 0

    def __init__(self, **kwargs):
        super().__init__("dummy", **kwargs)

    def temperature(self):
        """Returns the current temperature. It also updates the status. Locks for 10 ms to let the buffer update."""
        return self._temperature

    def rate(self, value):
        """Rate value in C°/min. Must be between 0 and 200"""
        pass

    def limit(self, value):
        """Maximum Temperature in C°. Must be between 0 and 1500"""
        self._temperature = value

    def start(self):
        """Starts the heating operation."""
        pass

    def stop(self):
        """Halts the current operation."""
        pass
