from Model.AnfatecDriver import AnfatecAMU24
import time

inst = AnfatecAMU24()
inst.pll = True
inst.set_lockin_time_constant(5)
inst.set_input_gain(10)
inst.set_lockin_harmonic(1)
time.sleep(1)
print(inst.amplitude.magnitude)
time.sleep(1)
print(inst.amplitude)
