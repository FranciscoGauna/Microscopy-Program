from datetime import datetime

import comtypes
import math
import comtypes.client
import plotly.graph_objects as go

from Drivers.DAQ.daq_driver import ComDaqBackend, ComDAQ
from time import sleep


def print_devices():
    program_id = comtypes.GUID("{DB9935C1-19C5-4ED2-ADD2-9A57E19F53A6}")
    lib = comtypes.client.CreateObject(program_id)
    print(lib.DeviceList())


def print_support():
    driver = ComDAQ()
    driver.initialize()
    print(driver.lib.AnalogInputs())


def set_point():
    driver = ComDAQ()
    driver.initialize()
    driver.set_analog_output(268435457, 0.2)
    sleep(10)
    print(driver.lib.AnalogOutputs())


def draw_wave():
    driver = ComDAQ()
    driver.initialize()
    driver.set_analog_wave(268435457, 0.2, 50, "SQR")
    sleep(10)
    print(driver.lib.AnalogOutputs())


def test():
    backend = ComDaqBackend(scan_rate=2000)
    print(datetime.now())
    sleep(0.5)
    backend.end()
    print(datetime.now())
    print(backend.daq._count)
    print(backend.data)
    fig = go.Figure(data=go.Scatter(x=[x for x in range(100)], y=backend.data[300:400]))
    fig.write_html("file.html")


if __name__ == "__main__":
    test()
