from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep
from typing import Dict, Generator, Any

from PyQt5.QtGui import QImage, QPixmap
from SER.interfaces import Instrument, ConfigurationUI, ConfigurableInstrument
from cv2 import cvtColor, COLOR_BGR2RGB
from lantz import Feat
from lantz.qt.connect import connect_feat

from components.CameraPlatina import CameraBackend
from components.CameraPlatina.calibration import CalibrationUI
from components.CameraPlatina.custom_image import ImageWidget, convert_coordinates
from components.Platina import Platina, PlatinaComponent


class CameraPlatinaInstrument(ConfigurableInstrument):

    def __init__(self, motor_x: Platina, motor_y: Platina, camera: CameraBackend):
        super(CameraPlatinaInstrument, self).__init__()
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.camera = camera
        self.square = True
        self.line = False

    def get_config(self) -> Dict:
        return {
            "motor_x": self.motor_x.get_config(),
            "motor_y": self.motor_y.get_config(),
            "square": self.square,
            "line": self.line
        } | super().get_config()

    def set_config(self, config: Dict):
        super().set_config(config)
        self.motor_x.set_config(config["motor_x"])
        self.motor_y.set_config(config["motor_y"])
        self.square = config["square"]
        self.line = config["line"]

    def variable_documentation(self) -> Dict[str, str]:
        motor_config = self.motor_x.variable_documentation()
        variables = {}
        for key, value in motor_config.items():
            variables[f"motor_{key}"] = value
        return motor_config

    def close_motors(self):
        self.motor_x.motor.close_motor()
        self.motor_y.motor.close_motor()

    def configure(self, x, y) -> Dict[str, Any]:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.motor_x.configure, x),
                executor.submit(self.motor_y.configure, y)
            ]

        results = {
            "motor_x": futures[0].result(),
            "motor_y": futures[1].result()
        }
        return results

    def get_points(self) -> Generator:
        if self.square:
            for x in self.motor_x.get_points():
                for y in self.motor_y.get_points():
                    yield *x, *y
        elif self.line:
            assert self.motor_x.point_amount() == self.motor_y.point_amount()
            x_iter = self.motor_x.get_points()
            for y in self.motor_y.get_points():
                yield *next(x_iter), *y

    def point_amount(self) -> int:
        if self.square:
            return self.motor_x.point_amount() * self.motor_y.point_amount()
        if self.line:
            return self.motor_x.point_amount()

    @Feat(values={True, False})
    def square_shape(self):
        return self.square

    @square_shape.setter
    def square_shape(self, value):
        self.square = value
        self.line = not value

    @Feat(values={True, False})
    def line_shape(self):
        return self.line

    @line_shape.setter
    def line_shape(self, value):
        self.line = value
        self.square = not value


class CameraPlatinaUI(ConfigurationUI):
    gui = "conf.ui"
    backend: CameraPlatinaInstrument
    calibration_dialog: CalibrationUI

    def __init__(self, motor_x: PlatinaComponent, motor_y: PlatinaComponent, parent=None, backend=None):
        super().__init__(parent, backend)

        self.motor_x = motor_x
        self.motor_y = motor_y

        self.widget.layout().addWidget(motor_x.conf_ui.widget)
        self.widget.layout().addWidget(motor_y.conf_ui.widget)

        self.motor_x.conf_ui.widget.setTitle("Motor X")
        self.motor_y.conf_ui.widget.setTitle("Motor Y")

        self.widget.square_rb.toggle()
        self.widget.square_rb.toggled.connect(self.toggleSquare)

        # TODO: this is kinda fugly, rethink maybe to a bool
        shape = "rectangle" if self.backend.square_shape else "line"
        pixmap = self.get_pixmap()
        self.image_widget = ImageWidget(pixmap, self.widget.image_label, self.parse_points, shape)
        self.widget.group_box.layout().insertWidget(0, self.image_widget)

        self.widget.calibrate_bt.pressed.connect(self.open_calibration)
        self.calibration_dialog = CalibrationUI(self.get_pos, pixmap)

        # Threading stuff
        self.camera_thread = Thread(target=self.take_pictures)
        self.running = True
        self.camera_thread.start()

    def get_pos(self):
        return self.motor_x.instrument.position(), self.motor_y.instrument.position()

    def get_pixmap(self) -> QPixmap:
        frame = self.backend.camera.snap()
        rgb_image = cvtColor(frame, COLOR_BGR2RGB)
        reconvert = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
        reconvert = QPixmap.fromImage(reconvert)
        # TODO: move these magic numbers to a place
        return QPixmap(reconvert).scaled(480, 320)

    def take_pictures(self):
        while self.running:
            pixmap = self.get_pixmap()
            self.image_widget.set_image(pixmap)
            self.calibration_dialog.set_image(pixmap)
            # TODO: change update timing
            sleep(0.5)

    def toggleSquare(self):
        self.backend.square_shape = not self.backend.square_shape
        if self.backend.square_shape:
            self.image_widget.draw_rect()
        else:
            self.image_widget.draw_line()

    def close_camera_refresh(self):
        self.running = False
        self.camera_thread.join()

    def parse_points(self, x1, y1, x2, y2):
        x1, y1 = convert_coordinates(x1, y1)
        x2, y2 = convert_coordinates(x2, y2)
        self.motor_x.instrument.initial_point = x1
        self.motor_x.instrument.final_point = x2
        self.motor_y.instrument.initial_point = y1
        self.motor_y.instrument.final_point = y2

    def open_calibration(self):
        self.calibration_dialog.open()
