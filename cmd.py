from Model.AnfatecDriver import AnfatecAMU24
import time

inst = AnfatecAMU24()
inst.pll = True
inst.set_lockin_time_constant(5)
inst.set_input_gain(10)
inst.harmonic = 1
inst.pll = False
time.sleep(1)
inst.lockin_amplitude = 10
inst.lockin_frequency = 1000
time.sleep(1)
print(inst.harmonic)
