import traceback
from time import sleep
from math import sqrt

from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtGui import QPixmap, QColor, QImage, QPainter
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
                sleep(0.002)
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
    qimage: QImage

    points = []

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self.min = self.max = self.test_point()

        # Initialization of the color spectrum and the image
        for i in range(self.spectrum_n):
            color = QColor()
            color.setRgb(self.color_list_base[i], 255, 0)
            self.color_list.append(color)
        for i in reversed(range(0, self.spectrum_n - 1)):
            color = QColor()
            color.setRgb(255, self.color_list_base[i], 0)
            self.color_list.append(color)
        self.create_colors()
        self.qimage = QImage(self.width(), self.height(), QImage.Format_RGB32)

        # Create sub-worker to reload image
        self.worker = LoaderWorker(self)
        self.worker.start()

    def width(self):
        return 200

    def height(self):
        return 200

    def test_point(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    # Aca empiezan el codigo del color
    def load_pixel_color(self, x, y, value):
        if value > self.max:
            self.max = value
            self.create_colors()
            self.recalculate_colors()
        if value < self.min:
            self.min = value
            self.create_colors()
            self.recalculate_colors()
        color = self.decide_color(value)
        self.points.append([x, y, value, color])
        self.qimage.setPixelColor(x, y, color)

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
            x = point[0]
            y = point[1]
            value = point[2]
            point[3] = self.decide_color(value)
            self.qimage.setPixelColor(x, y, point[3])


class ViewTestFt(Frontend):
    gui = ("..", "View", "frontend", "UI", "view_only_test.ui")

    backend: ViewTestBt
    scene: QGraphicsScene
    timer = QTimer()
    current_scale = 1

    def connect_backend(self):
        self.scene = QGraphicsScene(0, 0, self.backend.width(), self.backend.height())
        self.widget.map_view.setScene(self.scene)
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.load_points)
        self.timer.start()

    def load_points(self):
        try:
            pixmap = QPixmap()
            pixmap.convertFromImage(self.backend.qimage)
            g_pixmap = QGraphicsPixmapItem(pixmap)
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
