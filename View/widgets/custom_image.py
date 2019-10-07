from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from lantz.core.log import DEBUG


class ImageWidget(QWidget):
    pixmap = None
    draw_what = "point"
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    def __init__(self, pixmap: QPixmap):
        super().__init__()
        scale = pixmap.height() / pixmap.width()
        self.setFixedSize(640, int(640*scale))
        self.pixmap = pixmap

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


