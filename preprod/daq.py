import time
import comtypes
import comtypes.client

program_id = comtypes.GUID("{DB9935C1-19C5-4ED2-ADD2-9A57E19F53A6}")
lib = comtypes.client.CreateObject(program_id)
print(lib.SetDevice('DaqBoard3K0'))
print(lib.OpenDevice())
print(lib.DigitalOutputs())
print(lib.WriteDPort(0, 0, 255))
print(lib.WriteDPort(0, 1, 127))
print(lib.WriteDPort(0, 2, 127))

time.sleep(100)