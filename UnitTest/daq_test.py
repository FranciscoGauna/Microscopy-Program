from Drivers.DAQ.daq_driver import ComDAQ


def test():
    driver = ComDAQ()
    driver.initialize()


if __name__ == "__main__":
    test()
