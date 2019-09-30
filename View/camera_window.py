from lantz.qt import Frontend
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from Backend.camera_backend import CameraBackend
import cv2


class CameraControlUi(Frontend):
    backend: CameraBackend
    gui = ('frontend', 'UI', 'camera_button.ui')
    timer = QTimer()

    def connect_backend(self):
        self.timer.setInterval(15)
        self.timer.timeout.connect(self.take_photo)
        self.widget.snap_button.pressed.connect(self.start_stop)
        self.widget.image_label.mousePressEvent = self.getPos

    def getPos(self, event):
         x = event.pos().x()
         y = event.pos().y()
         print(x)
         print(y)

    def start_stop(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()


    def take_photo(self):
        frame = self.backend.snap()
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        reconvert = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
        reconvert = QPixmap.fromImage(reconvert)
        self.widget.image_label.setPixmap(QPixmap(reconvert))
