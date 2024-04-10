from os import path
from typing import Callable
import numpy as np
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QSpinBox, QDoubleSpinBox, QDialogButtonBox


class CalibrationInstance:
    transform_filename = path.join(path.dirname(path.realpath(__file__)), "camera_calibration.npy")

    def __init__(self, transform_filename=None):
        if transform_filename is not None:
            self.transform_filename = transform_filename

        self.transform_matrix = np.array((
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1)
        ), dtype=float)

        if path.exists(self.transform_filename):
            self.transform_matrix = np.load(self.transform_filename, fix_imports=False)

        self.inverse_matrix = np.linalg.inv(self.transform_matrix)

    def update_matrix(self, matrix: np.matrix):
        self.transform_matrix = matrix
        self.inverse_matrix = np.linalg.inv(matrix)

    def convert_coordinates(self, x, y):
        return tuple(np.matmul(np.array((x, y, 1)), self.transform_matrix))

    def invert_coordinates(self, x, y):
        return tuple(np.matmul(np.array((x, y, 1)), self.inverse_matrix))

    def store_calibration(self, transform_filename=None):
        if transform_filename is None:
            transform_filename = self.transform_filename
        np.save(transform_filename, self.transform_matrix, fix_imports=False)


class CalibrationUI(QDialog):
    image_label: QLabel
    display_label: QLabel
    zero_bt: QPushButton
    display_lt: QVBoxLayout
    data_points: list

    x1_pos_sb: QDoubleSpinBox
    x1_pixel_sb: QSpinBox
    y1_pos_sb: QDoubleSpinBox
    y1_pixel_sb: QSpinBox
    x2_pos_sb: QDoubleSpinBox
    x2_pixel_sb: QSpinBox
    y2_pos_sb: QDoubleSpinBox
    y2_pixel_sb: QSpinBox
    x3_pos_sb: QDoubleSpinBox
    x3_pixel_sb: QSpinBox
    y3_pos_sb: QDoubleSpinBox
    y3_pixel_sb: QSpinBox

    info_bt: QPushButton
    button_box: QDialogButtonBox

    def __init__(self, get_motor_positions: Callable[[], tuple[int, int]], pixmap: QPixmap):
        super().__init__()
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "calibration.ui")
        uic.loadUi(ui_file_path, self)

        self.get_motor_positions = get_motor_positions
        self.pixmap_width = 0
        self.pixmap_height = 0
        self.image_label.setAttribute(Qt.WA_MouseTracking)
        self.image_label.mouseMoveEvent = self.mouseMoveEvent
        self.image_label.mousePressEvent = self.mousePressEvent
        self.counter = 0

        self.data_points = [
            ((0, 0, 1), (0, 0, 1)),
            ((0, 0, 1), (0, 0, 1)),
            ((0, 0, 1), (0, 0, 1)),
        ]

        self.calibration = CalibrationInstance()
        self.new_matrix = self.calibration.transform_matrix
        self.button_box.accepted.connect(self.set_new_matrix)

        # TODO: another place to check for localization
        self.info_bt.setToolTip("Pasos para calibrar el motor con la camara: "
                                "\n - Clickear un punto en la muestra visto a traves de la camara"
                                "\n - Desplazar el motor en el eje X"
                                "\n - Clickear el mismo punto en la muestra visto en la camara"
                                "\n - Desplazar el motor en el eje Y"
                                "\n - Clickear el mismo punto en la muestra visto en la camara")

    def set_image(self, pixmap: QPixmap):
        self.image_label.setPixmap(pixmap)
        self.pixmap_width = pixmap.width()
        self.pixmap_height = pixmap.height()
        self.image_label.resize(self.pixmap_width, self.pixmap_height)

    def pixamap_center(self, x, y):
        return int(x - (self.pixmap_width / 2)), int(y - (self.pixmap_height / 2))

    def update_zero(self, x, y):
        self.calibration.transform_matrix[2][0] = x
        self.calibration.transform_matrix[2][1] = y
        self.calibration.update_matrix(self.calibration.transform_matrix)

    def convert_coordinates(self, x, y):
        x, y = self.pixamap_center(x, y)
        return self.calibration.convert_coordinates(x, y)

    def invert_coordinates(self, x, y):
        x, y, _ = self.calibration.invert_coordinates(x, y)
        return int(x + (self.pixmap_width / 2)), int(y + (self.pixmap_height / 2))

    def mouseMoveEvent(self, event: QMouseEvent):
        x, y = self.pixamap_center(event.pos().x(), event.pos().y())
        string = str(f"{x},{y}")
        self.display_label.setText(string)

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if 0 < x < self.pixmap_width and 0 < y < self.pixmap_height:
            x, y = self.pixamap_center(x, y)
            self.get_coords(x, y)

    def get_coords(self, x_pixel, y_pixel):
        try:
            x, y = self.get_motor_positions()
            print(f"Get x: {x} y: {y} x_pixel: {x_pixel} y_pixel: {y_pixel} counter: {self.counter}")
            self.data_points[self.counter] = ((-x_pixel, -y_pixel, 1), (x, y, 1))
            if self.counter == 0:
                self.x1_pos_sb.setValue(x)
                self.y1_pos_sb.setValue(y)
                self.x1_pixel_sb.setValue(x_pixel)
                self.y1_pixel_sb.setValue(y_pixel)
                self.counter += 1
            elif self.counter == 1:
                self.x2_pos_sb.setValue(x)
                self.y2_pos_sb.setValue(y)
                self.x2_pixel_sb.setValue(x_pixel)
                self.y2_pixel_sb.setValue(y_pixel)
                self.counter += 1
            else:
                self.x3_pos_sb.setValue(x)
                self.y3_pos_sb.setValue(y)
                self.x3_pixel_sb.setValue(x_pixel)
                self.y3_pixel_sb.setValue(y_pixel)
                self.counter = 0
            self.new_matrix = np.linalg.solve([x[0] for x in self.data_points], [x[1] for x in self.data_points])
            np.savetxt(sys.stdout, self.new_matrix, '%6.2f')
        except np.linalg.LinAlgError:
            print("failed to calculate value")

    def set_new_matrix(self):
        self.calibration.transform_matrix = self.new_matrix
        print("we have set the calibration matrix")
