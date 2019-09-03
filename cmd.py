from Model.AnfatecDriver import AnfatecAMU24
import time
import threading

inst = AnfatecAMU24()
inst.pll = True
inst.set_lockin_time_constant(2)
inst.set_input_gain(10)
inst.harmonic = 1

def func(inst):
    while(True):
        time.sleep(0.1)
        print(inst.amplitude.magnitude)
        print(inst.status)

func(inst)