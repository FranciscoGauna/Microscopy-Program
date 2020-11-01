import comtypes
import comtypes.client

from lantz import Driver
from lantz.qt import Backend


class ComDAQ(Driver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        program_id = comtypes.GUID("{DB9935C1-19C5-4ED2-ADD2-9A57E19F53A6}")
        self.lib = comtypes.client.CreateObject(program_id)
        print(self.lib.HelloWorld)
        print(self.lib.NewMethod)
        print(self.lib.DeviceList)
        print(self.lib.Echo("test"))


class ComDaqBackend(Backend):
    daq: ComDAQ

    def __init__(self):
        super().__init__()
        self.daq = ComDAQ()

    def focus(self):
        return True
