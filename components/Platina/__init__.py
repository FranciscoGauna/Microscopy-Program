from SER.interfaces import Component
from lantz.qt import wrap_driver_cls

from components.Platina.instrument_ui import PlatinaUI, Platina
from components.Platina.motor import Motor


class PlatinaComponent(Component):

    def __init__(self, motor: Motor):
        self.instrument = Platina(motor=motor)
        self.conf_ui = PlatinaUI(backend=self.instrument)