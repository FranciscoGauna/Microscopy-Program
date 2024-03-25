from typing import Callable

import numpy as np

from PyQt5.QtGui import QPainter, QPen, QPixmap, QMouseEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel

# TODO: change where we read the transform unit and translation unit
transform_matrix = np.identity(1)
translate_matrix = np.array([0, 0])


def convert_coordinates(x, y):
    return (np.array([x, y]) * transform_matrix + translate_matrix)[0]


class ImageWidget(QWidget):
    pixmap = None
    path_type = "none"
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    def __init__(self, pixmap: QPixmap, line_edit: QLabel, callback: Callable[[int, int, int, int], None], path_type="rectangle"):
        super().__init__()
        self.size = pixmap.width(), pixmap.height()
        self.setFixedSize(*self.size)
        self.pixmap = pixmap

        self.set_points: Callable[[int, int, int, int], None] = callback

        self.path_type = path_type
        self.flag_first_click = True

        self.line_edit = line_edit
        self.setAttribute(Qt.WA_MouseTracking)

    def set_image(self, pixmap):
        self.pixmap = pixmap
        self.update()

    def draw_line(self):
        self.path_type = "line"
        self.update()

    def draw_rect(self):
        self.path_type = "rectangle"
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.pixmap
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        if self.path_type == "line":
            painter.drawLine(self.x1, self.y1, self.x2, self.y2)
        elif self.path_type == "rectangle":
            start_x = min(self.x1, self.x2)
            start_y = min(self.y1, self.y2)
            width = abs(self.x1 - self.x2)
            height = abs(self.y1 - self.y2)
            painter.drawRect(start_x, start_y, width, height)
        else:
            pass

    def mouseMoveEvent(self, event: QMouseEvent):
        string = str(event.pos().x()) + "," + str(event.pos().y())
        self.line_edit.setText(string)

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.flag_first_click:
            self.x1 = x
            self.y1 = y
        else:
            self.x2 = x
            self.y2 = y
        self.flag_first_click = not self.flag_first_click
        x1, y1 = convert_coordinates(self.x1, self.y1)
        x2, y2 = convert_coordinates(self.x1, self.y1)
        self.set_points(self.x1, self.x2, self.y1, self.y2)
