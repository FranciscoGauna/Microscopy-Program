from lantz.qt import Backend, InstrumentSlot

class CameraBackend(Backend):

    def __init__(self, camera):
        self.camera = camera

    def snap(self):
        ret, frame = self.camera.read()
        if ret:
            return frame
        return [0, 0, 0]
