from copy import deepcopy
from PyIOTech import daq, daqh

import comtypes
import comtypes.client
import threading
import pause
from datetime import datetime, timedelta

from lantz import Driver, Feat, errors
from lantz.qt import Backend


class DaqBoard3k0(Driver):
    """
    This class provides a wrapper for the functions on the pyiotech library, plus a compendium of useful information
    about the library and it's methods
    """
    device_name = b"DaqBoard3K0"

    def __init__(self, *args, **kwargs):
        self.gain = daqh.DgainX1
        self.flags = daqh.DafAnalog | daqh.DafUnsigned | daqh.DafBipolar | daqh.DafDifferential
        self.max_voltage = 10.0
        self.bit_depth = 16
        self.device = None

        super().__init__(*args, **kwargs)

    def initialize(self):
        """Opens the device, this is important to be run before the execution of the driver."""
        super().initialize()
        self.device = daq.daqDevice(self.device_name)

    def set_analog(self, channel, ):
        pass

    def read_analog(self, channel):
        return self.device.AdcRd(channel, self.gain, self.flags)
