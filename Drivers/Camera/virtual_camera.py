import cv2

class VirtualCamera(cv2.VideoCapture):
    exposure = 5
    image = cv2.imread("UnitTest/test.png")

    def read(self):
        return True, self.image

    def get(self, key):
        return self.exposure

    def set(self, key, value):
        self.exposure = value