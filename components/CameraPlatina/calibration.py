from os import path
from typing import Callable
import numpy as np

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QSpinBox, QDoubleSpinBox

# TODO: change where we read the transform matrix to a file and default to this
transform_matrix = np.array((
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1)
), dtype=float)


def convert_coordinates(x, y):
    return tuple(np.matmul(np.array((x, y, 1)), transform_matrix))


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

    def __init__(self, get_motor_positions: Callable[[], tuple[int, int]], pixmap: QPixmap):
        super().__init__()
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "calibration.ui")
        uic.loadUi(ui_file_path, self)

        self.get_motor_positions = get_motor_positions
        self.image_label.mouseMoveEvent = self.mouseMoveEvent
        self.image_label.mousePressEvent = self.mousePressEvent
        self.counter = 0

        self.data_points = [
            ((0, 0, 1), (0, 0, 1)),
            ((0, 0, 1), (0, 0, 1)),
            ((0, 0, 1), (0, 0, 1)),
        ]

    def set_image(self, pixmap):
        self.image_label.setPixmap(pixmap)

    def mouseMoveEvent(self, event: QMouseEvent):
        string = str(event.pos().x()) + "," + str(event.pos().y())
        self.display_label.setText(string)

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        self.get_coords(x, y)

    def get_coords(self, x_pixel, y_pixel):
        try:
            x, y = self.get_motor_positions()
            print(f"Get x: {x} y: {y} x_pixel: {x_pixel} y_pixel: {y_pixel} counter: {self.counter}")
            self.data_points[self.counter] = ((x_pixel, y_pixel, 1), (x, y, 1))
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
            new_matrix = np.linalg.solve([x[0] for x in self.data_points], [x[1] for x in self.data_points])
            transform_matrix.data = new_matrix.data
            print(new_matrix)
        except np.linalg.LinAlgError:
            print("failed to calculate value")
