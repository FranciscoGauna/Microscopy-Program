from Drivers.DAQ.daq_driver import ComDAQ


def test():
    driver = ComDAQ()
    driver.initialize()
    driver.write_analog(5, 1)


if __name__ == "__main__":
    test()
