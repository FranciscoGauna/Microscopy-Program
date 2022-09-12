from copy import deepcopy

import comtypes
import comtypes.client
import threading
import pause
from datetime import datetime, timedelta

from lantz import Driver, Feat, errors
from lantz.qt import Backend


class ComDAQ(Driver):
    """
    This class provides a wrapper for the functions on the ddl for the DAQ com server. This is necessary because the
    library is only available in 32 bits and this allows us to call it in a 64 process using the processs intercom from
    windows
    """
    device_name = "DaqBoard3K0"

    def __init__(self, *args, **kwargs):
        self.started = False
        program_id = comtypes.GUID("{DB9935C1-19C5-4ED2-ADD2-9A57E19F53A6}")
        self.lib = comtypes.client.CreateObject(program_id)
        self._scan_rate = kwargs.pop('scan_rate', 100)
        self._count = 0

        super().__init__(*args, **kwargs)

    def __del__(self):
        """When the object is deleted it sends the signal to the COMServer stop scanning to the daq."""
        self.stop_scan()
        del self.lib

    def initialize(self):
        """Opens the device, this is important to be run before the execution of the driver."""
        super().initialize()
        self.lib.SetDevice(self.device_name)
        if not self.lib.OpenDevice():
            raise errors.InstrumentError("The Device is not detected. If it's connected, check the DaqX Configuration "
                                         "Utility")

    def start_scan(self):
        """Starts scanning the ports that where set up in the methods 'set_analog_input' 'set_analog_output'
        """
        self.started = True
        self.lib.StartScanning(100, self._scan_rate)

    def stop_scan(self):
        """Stops the scan and extra thread"""
        if self.started:
            self.lib.StopScanning()
        self.started = False

    @Feat(units='Hz')
    def scan_rate(self):
        """Property that indicates the speed of the scan rate of the device in Hz. It's better to put them as high as
        possible to reduce the amount of com communications."""
        return self._scan_rate

    @scan_rate.setter
    def scan_rate(self, value):
        self._scan_rate = value

    def set_analog_input(self, channel):
        if self.started:
            return
        if not self.lib.SetAnalogInput(channel):
            raise errors.InstrumentError("This channel is not supported, check the documentation for the available "
                                         "outputs for your card")

    def set_analog_output(self, channel, value):
        self.lib.SetAnalogOutput(channel, value)

    def set_analog_wave(self, channel, value, freq, wave="SIN"):
        if not self.lib.SetAnalogOutputWave(channel, value, freq, wave):
            raise errors.InstrumentError("This channel is not supported, check the documentation for the available "
                                         "outputs for your card")

    def write_analog(self, port, value):
        print(self.lib.WriteAPort(port, value))

    def read_analog(self):
        """
        read the analog inputs that were set up before started scannign
        :return:
        """
        self._count += 1
        results = self.lib.ReadAPort()
        if len(results) == 0:
            return [float("NaN")]
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

    def __init__(self, scan_rate=100):
        super().__init__()
        self.data = []
        self.daq = ComDAQ(scan_rate=scan_rate)
        self.daq.initialize()
        self.daq.set_analog_input(5)
        self.delta = timedelta(seconds=(1 / self.daq.scan_rate.magnitude))
        self.timer = threading.Thread(target=self.run)
        self.time = datetime.now()
        self.timer.start()

    def focus(self):
        return True

    def end(self):
        self.started = False
        self.lock.acquire()
        self.daq.stop_scan()
        self.lock.release()
        return

    def run(self):
        comtypes.CoInitialize()
        self.daq.start_scan()
        while self.started:
            self.lock.acquire()
            self.data.extend(self.daq.read_analog())
            self.lock.release()
            self.time += self.delta
            pause.until(self.time)

