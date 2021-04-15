import comtypes
import comtypes.client

from lantz import Driver
from lantz.qt import Backend


class ComDAQ(Driver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        program_id = comtypes.GUID("{DB9935C1-19C5-4ED2-ADD2-9A57E19F53A6}")
        self.lib = comtypes.client.CreateObject(program_id)

    def __del__(self):
        del self.lib

    def initialize(self):
        super().initialize()
        self.lib.SetDevice("DaqBoard3K0")
        self.lib.OpenDevice()
        self.lib.SetAnalogInput()
        self.lib.SetAnalogOutput()

    def write_analog(self, port, value):
        print(self.lib.WriteAPort(port, value))

    def read_analog(self, port):
        print(self.lib.ReadAPort(port))


class ComDaqBackend(Backend):
    daq: ComDAQ

    def __init__(self):
        super().__init__()
        self.daq = ComDAQ()

    def focus(self):
        return True
