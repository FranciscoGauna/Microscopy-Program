from os import path
from typing import Callable
import numpy as np

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QSpinBox, QDoubleSpinBox

from .custom_image import ImageWidget, transform_matrix, translate_matrix


class CalibrationUI(QDialog):
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

    def __init__(self, get_motor_positions: Callable[[], tuple[int, int]], pixmap: QPixmap):
        super().__init__()
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "calibration.ui")
        uic.loadUi(ui_file_path, self)

        self.get_motor_positions = get_motor_positions
        self.image_widget = ImageWidget(pixmap, self.display_label, self.get_coords, "none")
        self.display_lt.insertWidget(0, self.image_widget)

        self.zero_bt.pressed.connect(self.zero)

        self.data_points = [(0, 0), (0, 0)]

    def zero(self):
        x, y = self.get_motor_positions()
        translate_matrix[0] = x
        translate_matrix[1] = y

    def set_image(self, pixmap):
        self.image_widget.set_image(pixmap)

    def get_coords(self, x1, y1, x2, y2):
        try:
            x, y = self.get_motor_positions()
            x -= float(translate_matrix[0])
            y -= float(translate_matrix[1])
            if not self.image_widget.flag_first_click:
                self.data_points[0] = (x, y)
                self.x1_pos_sb.setValue(x)
                self.y1_pos_sb.setValue(y)
            else:
                self.data_points[1] = (x, y)
                self.x2_pos_sb.setValue(x)
                self.y2_pos_sb.setValue(y)
            self.x1_pixel_sb.setValue(x1)
            self.y1_pixel_sb.setValue(y1)
            self.x2_pixel_sb.setValue(x2)
            self.y2_pixel_sb.setValue(y2)
            a_1 = (x1, y1)
            a_2 = (x2, y2)
            new_matrix = np.linalg.solve([a_1, a_2], self.data_points)
            transform_matrix.data = new_matrix.data
            print(new_matrix)
        except np.linalg.LinAlgError:
            print("failed to get value")