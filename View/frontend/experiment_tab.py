import traceback

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from lantz.qt import Frontend

from Backend.experiment_backend import ExperimentBackend
from Model.run_experiment import ProgressBarController


class ExperimentTab(Frontend):
    gui = ("UI", "experiment_tab.ui")
    backend: ExperimentBackend
    scene: QGraphicsScene
    g_pixmap: QGraphicsPixmapItem
    pregress_bar_controller: ProgressBarController
    view_timer = QTimer()

    def setupUi(self):
        pass

    def connect_backend(self):
        self.scene = QGraphicsScene(0, 0, 200, 200)
        self.widget.map_view.setScene(self.scene)
        self.pregress_bar_controller = ProgressBarController(self.widget.exp_bar, self.widget.start_bt,
                                                             self.backend.worker,
                                                             self.widget.current_le)

        self.view_timer.setInterval(30)
        self.view_timer.timeout.connect(self.load_points)
        self.view_timer.start()

    def load_points(self):
        try:
            pixmap = QPixmap()
            pixmap.convertFromImage(self.pregress_bar_controller.qimage())

            if hasattr(self, "g_pixmap"):
                self.scene.removeItem(self.g_pixmap)
            self.g_pixmap = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.g_pixmap)
        except:
            traceback.print_exc()