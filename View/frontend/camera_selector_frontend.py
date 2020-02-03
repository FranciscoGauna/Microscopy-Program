import cv2
from Model.virtual_camera import VirtualCamera

from lantz.qt import Frontend
from View.localization import locale


class CameraSelectorFrontend(Frontend):
    gui = ("UI", "camera_selector.ui")

    def setupUi(self):
        self.widget.camera_rb.setText(locale.get("virtual_camera", "str_virtual_camera"))

    def camera(self) -> cv2.VideoCapture:
        return cv2.VideoCapture(0) if not self.widget.camera_rb.isChecked() else VirtualCamera()
