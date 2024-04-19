from lantz import log
from lantz.core import MessageBasedDriver
from pyvisa.constants import StopBits, Parity
from time import sleep

from components.Oven.TMS94 import T94Driver

log.log_to_screen(log.DEBUG)


horno = T94Driver.via_serial("15")
horno.initialize()
print(horno.temperature())
print(horno.status)
horno.finalize()
print(horno)
