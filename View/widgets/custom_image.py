from PyQt5.QtGui import QPainter, QPen, QPixmap, QHoverEvent, QMouseEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from lantz.core.log import DEBUG

from Model.scaler import lin_list


class ImageWidget(QWidget):
    pixmap = None
    draw_what = "point"
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    x_steps = 2
    y_steps = 2

    def __init__(self, pixmap: QPixmap, line_edit):
        super().__init__()
        scale = pixmap.height() / pixmap.width()
        self.setFixedSize(640, int(640*scale))
        self.pixmap = pixmap
        self.line_edit = line_edit

        self.setAttribute(Qt.WA_MouseTracking)

    def set_image(self, pixmap):
        self.pixmap = pixmap
        self.update()

    def draw_point(self, x1, x2):
        self.draw_what = "point"
        self.x1 = x1
        self.x2 = x2
        self.update()

    def draw_line(self, x1, x2, y1, y2):
        self.draw_what = "line"
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.update()

    def draw_rect(self, x1, x2, y1, y2):
        self.draw_what = "rectangle"
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = self.pixmap
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        if self.draw_what is "point":
            painter.drawPoint(self.x1, self.x2)
        elif self.draw_what is "line":
            painter.drawLine(self.x1, self.y1, self.x2, self.y2)
        elif self.draw_what is "rectangle":
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
