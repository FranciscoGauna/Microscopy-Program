import sys
from PyQt5.QtWidgets import QApplication
newApp = QApplication(sys.argv)
from Backend.camera_backend import CameraBackend
from View.camera_window import CameraWindow
from lantz.qt import start_gui_app
import cv2


cv2.destroyAllWindows()
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    cap.release()
    cv2.destroyAllWindows()
    raise Exception("The camera isn't plugged in")

app = CameraBackend(cap)
start_gui_app(app, CameraWindow)

cap.release()
cv2.destroyAllWindows()
