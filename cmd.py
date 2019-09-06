from Model.AnfatecDriver import AnfatecAMU24, Coupling
import time
from lantz import Q_
from lantz.core.log import log_to_screen, INFO

#log_to_screen(INFO)
inst = AnfatecAMU24()
inst.pll = False

def func(inst):
    while True:
        for t in range(0, 5):
            time.sleep(0.5)
            print(inst.amplitude.magnitude)
        print(inst.status)
        inst.pll = not inst.pll
        inst.set_lockin_time_constant(0)
        inst.lockin_frequency = Q_(100,"Hz")
        inst.coupling = Coupling.ac
        print(inst.pll)


func(inst)
