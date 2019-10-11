import cv2
from lantz.qt import Backend
from lantz.core import Feat


class CameraBackend(Backend):

    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def snap(self):
        ret, frame = self.camera.read()
        if ret:
            return frame
        return [0, 0, 0]

    @Feat()
    def exposure(self):
        return self.camera.get(cv2.CAP_PROP_EXPOSURE)

    @exposure.setter
    def exposure(self, time):
        self.camera.set(cv2.CAP_PROP_EXPOSURE, -time)
