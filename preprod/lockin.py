from json import dump
from time import sleep

from lantz import Q_

from components.Lockin.anfatec_driver import AnfatecAMU24, Coupling

lockin = AnfatecAMU24()
lockin.initialize()
lockin.pll = False
lockin.lockin_roll_off = "6dB/oct"
lockin.time_constant = "10 ms"
lockin.coupling = Coupling.dc
results = []
for i in range(100):
    freq = 7500 + i * 50
    lockin.lockin_frequency = Q_(freq, "hertz")
    sleep(0.010)
    results.append(lockin.lib._GetLockInChannel(2))


with open("results.json", "w+") as file:
    dump(results, file)
