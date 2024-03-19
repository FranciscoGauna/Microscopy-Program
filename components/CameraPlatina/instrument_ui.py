from threading import Thread
from time import sleep
from typing import Dict

from PyQt5.QtGui import QImage, QPixmap
from SER.interfaces import Instrument, ConfigurationUI
from cv2 import cvtColor, COLOR_BGR2RGB

from components.Camera.instrument_ui import CameraBackend
from components.Platina import Platina


class CameraPlatinaInstrument(Instrument):
    def __init__(self, motor_x: Platina, motor_y: Platina, camera: CameraBackend):
        super(CameraPlatinaInstrument, self).__init__()
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.camera = camera


    def get_config(self) -> Dict:
        return {
            "motor_x": self.motor_x.get_config(),
            "motor_y": self.motor_y.get_config()
        }

    def set_config(self, config: Dict):
        self.motor_x.set_config(config["motor_x"])
        self.motor_y.set_config(config["motor_y"])
        self.camera.set_config(config["camera"])

    def variable_documentation(self) -> Dict[str, str]:
        motor_config = self.motor_x.variable_documentation()
        variables = {}
        for key, value in motor_config.items():
            variables[f"motor_{key}"] = value
        return motor_config

    def close_motors(self):
        self.motor_x.motor.close_motor()
        self.motor_y.motor.close_motor()


class CameraPlatinaUI(ConfigurationUI):
    gui = "conf.ui"
    backend: CameraPlatinaInstrument

    def __init__(self, motor_x, motor_y, parent=None, backend=None):
        super().__init__(parent, backend)

        self.widget.layout().addWidget(motor_y.conf_ui.widget)
        self.widget.layout().addWidget(motor_x.conf_ui.widget)

        # Threading stuff
        self.camera_thread = Thread(target=self.take_pictures)
        self.running = True
        self.camera_thread.start()

    def take_pictures(self):
        while self.running:
            frame = self.backend.camera.snap()
            rgb_image = cvtColor(frame, COLOR_BGR2RGB)
            reconvert = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
            reconvert = QPixmap.fromImage(reconvert)
            pixmap = QPixmap(reconvert)
            self.widget.image_dp.setPixmap(pixmap)
            # TODO: change update timing
            sleep(0.5)

    def close_camera_refresh(self):
        self.running = False
        self.camera_thread.join()
