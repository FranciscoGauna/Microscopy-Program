from Drivers.DAQ.daq_driver import ComDAQ
from time import sleep


def test():
    driver = ComDAQ()
    driver.initialize()
    while 1:
        sleep(1)
        driver.read_analog(1)
        dbcDaqDirectOutput0 = 268435456
        dbcDaqDirectOutput1 = 268435457
        dbcDaqDirectOutput2 = 268435458
        dbcDaqDirectOutput3 = 268435459


if __name__ == "__main__":
    test()
