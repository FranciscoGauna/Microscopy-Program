import traceback
from time import sleep
from math import sqrt

from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from lantz.qt import Backend, Frontend, start_gui_app

from Model.scaler import lin_list, square_list


class LoaderWorker(QThread):
    def __init__(self, obj, parent=None):
        QThread.__init__(self, parent)
        self.obj = obj

    def run(self) -> None:
        try:
            while True:
                self.obj.load_value()
                sleep(0.001)
        except:
            traceback.print_exc()


class ViewTestBt(Backend):
    x = 0
    y = 0

    max: float
    min: float
    spectrum_n = 20
    color_list_base = square_list(0, 255, spectrum_n)
    color_list = []
    color_value_list = []
    recalculated = False

    points = []

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self.min = self.max = self.test_point()

        for i in range(self.spectrum_n):
            color = QColor()
            color.setRgb(self.color_list_base[i], 255, 0)
            self.color_list.append(color)
        for i in reversed(range(0, self.spectrum_n - 1)):
            color = QColor()
            color.setRgb(255, self.color_list_base[i], 0)
            self.color_list.append(color)

        self.create_colors()
        self.worker = LoaderWorker(self)
        self.worker.start()

    def width(self):
        return 200

    def lenght(self):
        return 200

    def test_point(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def read_point(self):
        offset_x = offset_y = 40
        result = sqrt(pow(self.x - offset_x, 2) + pow(self.y - offset_y, 2))
        self.x += 1
        if self.x >= 200:
            self.x = 0
            self.y += 1
            if self.y >= 200:
                self.y = 0
        return result

    # Aca empiezan el codigo del color
    def load_value(self):
        try:
            x = self.x
            y = self.y
            value = self.read_point()
            if value > self.max:
                self.max = value
                self.create_colors()
                self.recalculate_colors()
            if value < self.min:
                self.min = value
                self.create_colors()
                self.recalculate_colors()

            self.points.append([x, y, value, self.decide_color(value)])
        except:
            traceback.print_exc()

    def create_colors(self):
        result = []
        value_list = lin_list(self.min, self.max, self.spectrum_n * 2)
        for i in range(0, (self.spectrum_n * 2)-1):
            result.append((value_list[i+1], self.color_list[i]))
        self.color_value_list = result

    def decide_color(self, value):
        i = 0
        length = len(self.color_value_list)
        while i < length and value > self.color_value_list[i][0]:
            i += 1
        if i == length:
            i = length - 1
        return self.color_value_list[i][1]

    def recalculate_colors(self):
        for point in self.points:
            value = point[2]
            point[3] = self.decide_color(value)
        self.recalculated = True


class ViewTestFt(Frontend):
    gui = ("..", "View", "frontend", "UI", "view_only_test.ui")

    backend: ViewTestBt
    scene: QGraphicsScene
    timer = QTimer()
    g_points = {}
    current_scale = 1

    def connect_backend(self):
        self.scene = QGraphicsScene(0, 0, self.backend.width(), self.backend.lenght())
        self.widget.map_view.setScene(self.scene)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self.load_points)
        self.timer.start()

    def load_points(self):
        try:
            for point in self.backend.points:
                x = point[0]
                y = point[1]
                value = point[2]
                color = point[3]

                pixmap = QPixmap(1, 1)
                pixmap.fill(color)
                g_pixmap = QGraphicsPixmapItem(pixmap)
                g_pixmap.setOffset(x, y)
                if x not in self.g_points:
                    self.g_points[x] = {}
                self.g_points[x][y] = (value, g_pixmap)
                self.scene.addItem(g_pixmap)
        except:
            traceback.print_exc()

    def wheelEvent(self, event):
        try:
            num_pix = event.angleDelta()
            angle = num_pix.y()
            if angle > 0:
                self.widget.map_view.scale(2, 2)
            if angle < 0:
                self.widget.map_view.scale(1 / 2, 1 / 2)
        except:
            traceback.print_exc()


def run():
    app = ViewTestBt()
    start_gui_app(app, ViewTestFt)
