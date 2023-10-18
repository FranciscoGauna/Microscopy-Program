from ctypes import CDLL, byref, Structure, c_void_p, c_char, POINTER, WinDLL, c_int
from ctypes.wintypes import DWORD, LPDWORD
from os import path
from time import sleep
from typing import Optional


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

    def __init__(self, library: WinDLL, ft_handle: c_void_p, read_term, write_term):
        self.library = library
        self.handle = ft_handle
        self.read_term = read_term
        self.write_term = write_term

    def set_timeout(self, milliseconds: int):
        assert self.library.FT_SetTimeouts(self.handle, milliseconds, milliseconds) == 0

    def status(self) -> tuple[int, int, int]:
        read_len = DWORD()
        send_len = DWORD()
        event_status = DWORD()
        assert self.library.FT_GetStatus(self.handle, byref(read_len), byref(send_len), byref(event_status)) == 0
        return read_len.value, send_len.value, event_status.value

    def read(self, termination="\n", encoding="utf-8") -> str:
        """Blocking"""
        termination = self.read_term if termination is None else termination
        if encoding is None:
            encoding = "utf-8"
        term_byte = termination.encode(encoding)

        buffer = b""
        char = c_char()
        amount = DWORD()
        while char.value != term_byte:
            assert self.library.FT_Read(self.handle, byref(char), 1, byref(amount)) == 0
            if amount.value == 0:
                break

            buffer += char.value
        return buffer.decode(encoding).rstrip(termination)

    def write(self, message: str, termination: str = None, encoding: str = None):
        termination = self.write_term if termination is None else termination
        if encoding is None:
            encoding = "utf-8"
        term = b""
        if message[:2] != "++" and len(termination) > 0:
            term = b"\x1b" + termination.encode(encoding)
        message_bytes = message.encode(encoding) + term + b"\n"
        amount = DWORD()
        assert self.library.FT_Write(self.handle, message_bytes, len(message_bytes), byref(amount)) == 0
        assert amount.value == len(message_bytes)
        return amount.value

    def __del__(self):
        self.write("++clr")
        self.library.FT_Close(self.handle)


class FTD2XXWrapper:
    # Download the dll from ft chips

    def __init__(self, dll_location=path.dirname(path.realpath(__file__)) + ".\\ftd2xx64.DLL"):
        self.library = setup_dll(dll_location)

    def list_devices(self) -> list[DeviceInfo]:
        amount = DWORD()
        assert self.library.FT_CreateDeviceInfoList(byref(amount)) == 0
        devices = (DeviceInfo * amount.value)()

        assert self.library.FT_GetDeviceInfoList(devices, byref(amount)) == 0

        return [device for device in devices]

    def open(self, index: int, read_term: str, write_term: str) -> FTD2XXDevice:
        ft_handle = c_void_p()

        res = self.library.FT_Open(index, byref(ft_handle))
        assert res == 0, f"Res {res} isn't 0"

        return FTD2XXDevice(self.library, ft_handle, read_term, write_term)


if __name__ == "__main__":
    wrap = FTD2XXWrapper()
    for d in wrap.list_devices():
        pass
        #print_struct(d)
    dev = wrap.open(0, "\n", "")
    dev.set_timeout(100)
    dev.write("++ver")
    print(dev.read())
