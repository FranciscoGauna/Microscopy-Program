from os import path

import cv2
try:
    from lucam import Lucam
except FileNotFoundError:
    # We can't use it in case
    pass
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
        This method reads the sensor of the camera. If the camera failed to take a picture returs [[0,0,0]]

        :return: A frame of the camera
        """
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        return [[0, 0, 0]]

    @Feat()
    def exposure(self):
        """Exposure is a parameter that sets the exposure of the camera. This method returns the exposure"""
        return abs(self.camera.get(cv2.CAP_PROP_EXPOSURE))

    @exposure.setter
    def exposure(self, time):
        """Exposure is a parameter that sets the exposure of the camera. This method sets the exposure"""
        self.camera.set(cv2.CAP_PROP_EXPOSURE, -time)


class VirtualCamera(cv2.VideoCapture):
    """
        A class that recreates a cv2.VideoCapture class to test the app when no web-cam is connected
    """
    exposure = 5
    image = cv2.imread(path.join(path.dirname(path.realpath(__file__)), "test.png"))

    def read(self, image=None):
        """
            read([, image]) -> retval, image
                @brief Grabs, decodes and returns the next video frame.

                @return tuple of a boolean and an cv2 image
                the boolean indicates if it can be read
                the cv2 image what the camera sees
        """
        return True, self.image

    def get(self, key):
        """
            get(propId) -> retval
                @brief Returns the specified VideoCapture property
                the program uses only exposure with key value cv2.CAP_PROP_EXPOSURE

                @return value of the property
        """
        return self.exposure

    def set(self, key, value):
        """
            set(propId, value) -> retval
                @brief Sets a property in the VideoCapture.

                @param key Property identifier from cv.VideoCaptureProperties (only. cv2.CAP_PROP_EXPOSURE is used)
                @param value Value of the property.
        """
        if key == cv2.CAP_PROP_EXPOSURE:
            self.exposure = value


class LucamCam(cv2.VideoCapture):
    def __init__(self):
        super().__init__()
        self.camera = Lucam()
        self.image_format = self.camera.GetStillImageFormat()

    def read(self, image=None):
        """
            read([, image]) -> retval, image
                @brief Grabs, decodes and returns the next video frame.

                @return tuple of a boolean and an cv2 image
                the boolean indicates if it can be read
                the cv2 image what the camera sees
        """
        image = self.camera.TakeSnapshot()
        converted_image = self.camera.ConvertFrameToRGB24Ex(image, self.image_format)
        return True, converted_image

    def get(self, key):
        """
            get(propId) -> retval
                @brief Returns the specified VideoCapture property
                the program uses only exposure with key value cv2.CAP_PROP_EXPOSURE

                @return value of the property
        """
        return 0

    def set(self, key, value):
        """
            set(propId, value) -> retval
                @brief Sets a property in the VideoCapture.

                @param key Property identifier from cv.VideoCaptureProperties (only. cv2.CAP_PROP_EXPOSURE is used)
                @param value Value of the property.
        """
        pass

