from ctypes import CDLL, byref, Structure, c_void_p, c_char, POINTER, WinDLL, c_int
from ctypes.wintypes import DWORD, LPDWORD
from time import sleep


class DeviceInfo(Structure):
    _fields_ = [
        ("Flags", DWORD),
        ("Type", DWORD),
        ("ID", DWORD),
        ("LocId", DWORD),
        ("SerialNumber", c_char * 32),
        ("Description", c_char * 64),
        ("ftHandle", c_void_p)
    ]


def print_struct(struct: Structure):
    for field_name, field_type in struct._fields_:
        print(field_name, getattr(struct, field_name))


def setup_dll(dll_name: str) -> WinDLL:
    # We set up all the dll bullshit here
    library = WinDLL(dll_name)

    library.FT_CreateDeviceInfoList.argtypes = [LPDWORD]
    library.FT_CreateDeviceInfoList.restype = DWORD
    library.FT_GetDeviceInfoList.argtypes = [POINTER(DeviceInfo), LPDWORD]
    library.FT_GetDeviceInfoList.restype = DWORD
    library.FT_Open.argtypes = [c_int, c_void_p]
    library.FT_Open.restype = DWORD
    library.FT_Close.argtypes = [c_void_p]
    library.FT_Close.restype = DWORD
    library.FT_Read.argtypes = [c_void_p, POINTER(c_char), DWORD, LPDWORD]
    library.FT_Read.restype = DWORD
    library.FT_GetStatus.argtypes = [c_void_p, LPDWORD, LPDWORD, LPDWORD]
    library.FT_GetStatus.restype = DWORD
    library.FT_Write.argtypes = [c_void_p, POINTER(c_char), DWORD, LPDWORD]
    library.FT_Write.restype = DWORD
    library.FT_SetTimeouts.argtypes = [c_void_p, DWORD, DWORD]
    library.FT_SetTimeouts.restype = DWORD
    return library


class FTD2XXDevice:

    def __init__(self, library: WinDLL, ft_handle: c_void_p):
        self.library = library
        self.handle = ft_handle

    def set_timeout(self, milliseconds: int):
        assert self.library.FT_SetTimeouts(self.handle, milliseconds, milliseconds) == 0

    def status(self) -> tuple[int, int, int]:
        read_len = DWORD()
        send_len = DWORD()
        event_status = DWORD()
        assert self.library.FT_GetStatus(self.handle, byref(read_len), byref(send_len), byref(event_status)) == 0
        return read_len.value, send_len.value, event_status.value

    def read(self) -> str:
        """Blocking"""
        char = c_char()
        amount = DWORD()
        assert self.library.FT_Read(self.handle, byref(char), 1, byref(amount)) == 0
        if amount.value == 0:
            return ""

        read_backlog, _, _ = self.status()
        if read_backlog == 0:
            return char.value.decode('utf-8')

        buffer = (c_char * (read_backlog + 1))()
        assert self.library.FT_Read(self.handle, buffer, read_backlog, byref(amount)) == 0
        assert amount.value == read_backlog
        return (char.value + buffer.value).decode('utf-8')

    def write(self, message: str):
        message_bytes = message.encode('utf-8')
        amount = DWORD()
        assert self.library.FT_Write(self.handle, message_bytes, len(message_bytes), byref(amount)) == 0
        assert amount.value == len(message_bytes)

    def __del__(self):
        self.library.FT_Close(self.handle)


class FTD2XXWrapper:
    # Download the dll from ft chips

    def __init__(self, dll_name=".\\ftd2xx64.DLL"):
        self.library = setup_dll(dll_name)

    def list_devices(self) -> list[DeviceInfo]:
        amount = DWORD()
        assert self.library.FT_CreateDeviceInfoList(byref(amount)) == 0
        devices = (DeviceInfo * amount.value)()

        assert self.library.FT_GetDeviceInfoList(devices, byref(amount)) == 0

        return [device for device in devices]

    def open(self, index: int) -> FTD2XXDevice:
        ft_handle = c_void_p()

        res = self.library.FT_Open(index, byref(ft_handle))
        assert res == 0, f"Res {res} isn't 0"

        return FTD2XXDevice(self.library, ft_handle)


if __name__ == "__main__":
    wrap = FTD2XXWrapper()
    for d in wrap.list_devices():
        pass
        #print_struct(d)
    dev = wrap.open(0)
    dev.set_timeout(100)
    dev.write("++ver\n")
    print(dev.read())
