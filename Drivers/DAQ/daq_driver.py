import comtypes
import comtypes.client

from lantz import Driver


class VirtualDAQ(Driver):
    pass


class ComDAQ(Driver):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        program_id = comtypes.GUID("{DB9935C1-19C5-4ED2-ADD2-9A57E19F53A6}")
        self.lib = comtypes.client.CreateObject(program_id)
        print(self.lib.HelloWorld)
        print(self.lib.NewMethod)
        print(self.lib.DeviceList)
        print(self.lib.Echo("test"))
