from Model.AnfatecDriver import AnfatecAMU24
from lantz import Q_
from time import sleep

def frequency_scanner_linear(inst: AnfatecAMU24, start: int, end: int, step: int):
    """Scans the frequency range given linearly and stores the 4 channel values in the range of the lockin. The lockin
    should be preconfigured with the values you want to use."""
    if end < start:
        raise ValueError("End frequency should be bigger than start frequency")

    time_constant_list = [0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    inst.pll = False
    results = []
    while start < end:
        inst.lockin_frequency = Q_(start, "hertz")
        sleep(time_constant_list[inst.get_lockin_time_constant()]*0.001*10)
        results.append([])
        results[-1].append(start)
        results[-1].append(inst.real_part_x())
        results[-1].append(inst.imaginary_part_y())
        results[-1].append(inst.amplitude)
        results[-1].append(inst.phase)
        start += step

    return results
