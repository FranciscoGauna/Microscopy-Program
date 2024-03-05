from SER.interfaces import Component

from components.Platina.instrument_ui import PlatinaUI, Platina
from components.Platina.motor import Motor


class PlatinaComponent(Component):

    def __init__(self, motor: Motor, filename: str):
        self.instrument = Platina(motor=motor, filename=filename)
        self.conf_ui = PlatinaUI(backend=self.instrument)
