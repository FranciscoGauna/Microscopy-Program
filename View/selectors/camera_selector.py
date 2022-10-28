import cv2
from PyQt5.QtCore import Qt

from Drivers.Camera.virtual_camera import VirtualCamera

from lantz.qt import Frontend
from View.localization import locale
from config import config_file


class CameraSelector(Frontend):
    """
        This class provides the interface for the user and the program to select if you want to use a virtual camera
        or real camera.
    """

    gui = ("ui", "camera_selector.ui")

    def setupUi(self):
        self.widget.camera_cb.setText(locale.get("virtual_camera", "str_virtual_camera"))
        if config_file["PREVIOUS INSTRUMENTS"]["camera"] == "Virtual":
            self.widget.camera_cb.setCheckState(Qt.Checked)
        else:
            self.widget.camera_cb.setCheckState(Qt.Unchecked)

    def camera(self) -> cv2.VideoCapture:
        """
            @brief: This method returns a camera adapter object with the methods read, get and set, that recreate the
            functionality of cv2.VideoCapture
        """
        if self.widget.camera_cb.isChecked():
            config_file["PREVIOUS INSTRUMENTS"]["camera"] = "Virtual"
        else:
            config_file["PREVIOUS INSTRUMENTS"]["camera"] = "Webcam"
        return cv2.VideoCapture(0) if not self.widget.camera_cb.isChecked() else VirtualCamera()
