import cv2


class VirtualCamera(cv2.VideoCapture):
    """
        A class that recreates a cv2.VideoCapture class to test the app when no web-cam is connected
    """
    exposure = 5
    image = cv2.imread("UnitTest/test.png")

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
