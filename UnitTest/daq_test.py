from datetime import datetime

import comtypes
import math
import comtypes.client
import plotly.graph_objects as go
from Drivers.DAQ.daq_driver import DaqBoard3k0

from time import sleep


def test():
    driver = DaqBoard3k0()
    driver.initialize()
    data = []
    print(datetime.now())
    for x in range(1000):
        data.append(driver.read_analog(5))
        sleep(0.001)
    print(datetime.now())
    fig = go.Figure(data=go.Scatter(x=[x for x in range(100)], y=data[300:400]))
    fig.write_html("file.html")


if __name__ == "__main__":
    test()
