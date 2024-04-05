from SER.interfaces import Component

from components.Platina import PlatinaComponent
from components.Platina.motor import Motor
from .camera import CameraBackend, VirtualCamera
from .instrument_ui import CameraPlatinaInstrument, CameraPlatinaUI


class CameraPlatinaComponent(Component):
    # Has internal threads we need to close.
    instrument: CameraPlatinaInstrument
    conf_ui: CameraPlatinaUI

    def __init__(self, motor_x: PlatinaComponent, motor_y: PlatinaComponent, camera):
        self.instrument = CameraPlatinaInstrument(motor_x.instrument, motor_y.instrument, camera)
        self.conf_ui = CameraPlatinaUI(motor_x, motor_y, backend=self.instrument)

    def close_component(self):
        # TODO: add this to the component base class with a comment
        self.conf_ui.close_camera_refresh()
        self.instrument.close_motors()
