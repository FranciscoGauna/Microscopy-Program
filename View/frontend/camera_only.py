import cv2

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from lantz.qt import Frontend
from lantz.qt.app import start_frontend
from lantz.qt.connect import connect_feat

from Backend.camera_backend import CameraBackend
from View.localization import locale
from View.widgets.custom_image import ImageWidget


class CameraOnlyWindow(Frontend):
    backend: CameraBackend
    image: ImageWidget
    timer = QTimer()
    gui = ('UI', 'camera_only.ui')

    closed_target = None

    def setupUi(self):
        super().setupUi()
        try:
            self.widget.exposure_label.setText(locale.get("exposure", "str_exposure"))
        except Exception as e:
            print(e)

    def connect_backend(self):
        super().connect_backend()
        self.image = ImageWidget(self.take_photo(), self.widget.mouse_pos_le)
        self.widget.image_lt.addWidget(self.image)

        self.timer.setInterval(15)
        self.timer.timeout.connect(self.put_photo)
        self.timer.start()

        connect_feat(self.widget.exposure_time_input, self.backend, "exposure")

    def put_photo(self):
        self.image.set_image(self.take_photo())

    def take_photo(self):
        frame = self.backend.snap()
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        reconvert = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
        reconvert = QPixmap.fromImage(reconvert)
        pixmap = QPixmap(reconvert)
        return pixmap

    def closeEvent(self, event):
        if self.closed_target is not None:
            self.closed_target.toggle_camera()
        event.accept()

    def toggle_take_photos(self, boolean=None):
        if self.timer.isActive() != boolean:
            if self.timer.isActive():
                self.timer.stop()
                return False
            else:
                self.timer.start()
                return True
