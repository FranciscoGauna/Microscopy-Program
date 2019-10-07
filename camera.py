import sys
from PyQt5.QtWidgets import QApplication
newApp = QApplication(sys.argv)
from Backend.camera_backend import CameraBackend
from View.camera_window import CameraControlUi
from lantz.qt import start_gui_app
import cv2


cv2.destroyAllWindows()
cap = cv2.VideoCapture(0)

app = CameraBackend(cap)
start_gui_app(app, CameraControlUi)

cap.release()
cv2.destroyAllWindows()
