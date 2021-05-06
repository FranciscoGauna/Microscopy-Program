from datetime import datetime

from Drivers.DAQ.daq_driver import ComDaqBackend
from time import sleep


def test():
    backend = ComDaqBackend()
    print(datetime.now())
    for i in range(15):
        sleep(1)
        print(backend.data)
    print(datetime.now())
    print(backend.daq._count)


if __name__ == "__main__":
    test()
