from copy import deepcopy

import comtypes
import comtypes.client
import threading
import pause
from datetime import datetime, timedelta

pause.until(datetime(2015, 8, 12, 2))

from lantz import Driver, Feat
from lantz.qt import Backend


class ComDAQ(Driver):
    """
    This class provides a wrapper for the functions on the ddl for the DAQ com server. This is necessary because the
    library is only available in 32 bits and this allows us to call it in a 64 process using the processs intercom from
    windows
    """
    device_name = "DaqBoard3K0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.started = False
        program_id = comtypes.GUID("{DB9935C1-19C5-4ED2-ADD2-9A57E19F53A6}")
        self.lib = comtypes.client.CreateObject(program_id)
        self._scan_rate = 100
        self._count = 0

    def __del__(self):
        self.lib.StopScanning()
        del self.lib

    def initialize(self):
        super().initialize()
        self.lib.SetDevice(self.device_name)
        self.lib.OpenDevice()

    def start_scan(self):
        self.started = True
        self.lib.StartScanning(100, self._scan_rate)

    @Feat
    def scan_rate(self):
        return self._scan_rate

    @scan_rate.setter
    def scan_rate(self, value):
        self._scan_rate = value

    def set_analog_input(self, channel):
        if self.started:
            return
        self.lib.SetAnalogInput(channel)

    def set_analog_output(self, channel):
        self.lib.SetAnalogOutput(channel)

    def write_analog(self, port, value):
        print(self.lib.WriteAPort(port, value))

    def read_analog(self):
        """
        read the analog inputs that were set up before started scannign
        :return:
        """
        self._count += 1
        results = self.lib.ReadAPort().split(";")
        if results[0] == "fail":
            return []
        for i in range(0,len(results)):
            results[i] = float(results[i].replace(",", "."))
        return results


class ComDaqBackend(Backend):
    """
    This class provides the backend functions necessary to operate the daq inside the program
    """
    daq: ComDAQ
    timer: threading.Thread
    lock = threading.Lock()
    data: list
    started = True
    time: datetime
    delt: timedelta

    def get_data(self):
        self.lock.acquire()
        return_value = deepcopy(self.data)
        self.lock.release()
        return return_value

    def focus(self):
        return True

    def run(self):
        comtypes.CoInitialize()
        self.daq = ComDAQ()
        self.daq.initialize()
        self.daq.set_analog_input(5)
        self.delta = timedelta(seconds=(1 / self.daq.scan_rate))
        self.daq.start_scan()
        while self.started:
            self.lock.acquire()
            self.data = deepcopy(self.daq.read_analog())
            self.lock.release()
            self.time += self.delta
            pause.until(self.time)

    def __init__(self):
        super().__init__()
        self.data = []
        self.timer = threading.Thread(target=self.run)
        self.time = datetime.now()
        self.timer.start()
