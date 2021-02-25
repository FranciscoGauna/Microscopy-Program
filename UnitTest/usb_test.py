import usb.core
import usb.util
import libusb

libusb.config()

dev = usb.core.find(find_all=True)

# get next item from the generator
for d in dev:
    try:
        print(d)
    except:
        print("fail")
