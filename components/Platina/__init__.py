from SER.interfaces import Component

from components.Platina.instrument_ui import PlatinaUI, Platina
from components.Platina.motor import Motor


class PlatinaComponent(Component):

    # Has internal threads we need to close.

    def __init__(self, motor: Motor, filename: str, move_left_key="left", move_right_key="right"):
        self.instrument = Platina(motor=motor, filename=filename)
        self.conf_ui = PlatinaUI(self.instrument, move_left_key, move_right_key)

    def close_component(self):
        self.instrument.motor.close_motor()
