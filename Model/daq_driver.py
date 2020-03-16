import comtypes
import comtypes.client

progid = comtypes.GUID("{DB9935C1-19C5-4ed2-ADD2-9A57E19F53A3}")
com_class = comtypes.client.CreateObject(progid)
print(com_class.HelloWorld())
print(com_class.NewMethod())
print(com_class.DeviceList())
