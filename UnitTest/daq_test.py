from Drivers.DAQ.daq_driver import ComDAQ
from time import sleep


def test():
    driver = ComDAQ()
    driver.initialize()
    driver.write_analog(5, 1)
    while 1:
        sleep(1)


if __name__ == "__main__":
    test()
