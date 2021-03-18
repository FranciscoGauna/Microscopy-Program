from Drivers.Lockin.LI5655 import LI5655
import visa
from time import sleep, time


#_resource_manager = visa.ResourceManager()


def test():
    driver = LI5655.via_usb(serial_number="9280001")
    driver.initialize()
    driver.setup()

    driver.reference_internal = False

    print(driver.real_part_x)
    print(driver.imaginary_part_y)
    print(driver.amplitude)
    print(driver.phase)

    while 1:
        sleep(0.2)
        print(str(time()) + ": " + str(driver.phase))



if __name__ == "__main__":
    test()
