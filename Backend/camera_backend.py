import cv2
from lantz.qt import Backend
from lantz.core import Feat


class CameraBackend(Backend):
    """
    The Camera backend is a class with responsibility to administer the camera and offer an unified interface to
    interact with the camera to the program
    """
    camera: cv2.VideoCapture

    def __init__(self, camera: cv2.VideoCapture):
        """
        Initializes a backend.

        :param camera: The camera that is used by the backend
        """
        super().__init__()
        self.camera = camera

    def snap(self):
        """
        This method reads the sensor of the camera. If the camera failed to take a picture returs [0,0,0]

        :return: A frame of the camera
        """
        ret, frame = self.camera.read()
        if ret:
            return frame
        return [0, 0, 0]

    @Feat()
    def exposure(self):
        """Exposure is a a parameter that sets the exposure of the camera. This method returns the exposure"""
        return abs(self.camera.get(cv2.CAP_PROP_EXPOSURE))

    @exposure.setter
    def exposure(self, time):
        """Exposure is a a parameter that sets the exposure of the camera. This method sets the exposure"""
        self.camera.set(cv2.CAP_PROP_EXPOSURE, -time)
