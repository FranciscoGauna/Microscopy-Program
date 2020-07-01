import traceback
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from lantz.qt import Frontend
from lantz.qt.connect import connect_feat

from Backend.experiment_backend import ExperimentBackend
from Model.run_experiment import ProgressBarController
from View.localization import locale
from View.widgets.amp_chart import AmpChart, PhaseHistogram


class ExperimentTab(Frontend):
    gui = ("UI", "experiment_tab.ui")
    backend: ExperimentBackend

    amp_chart: AmpChart
    phase_chart: PhaseHistogram

    scene: QGraphicsScene
    g_pixmap: QGraphicsPixmapItem
    progress_bar_controller: ProgressBarController
    view_timer = QTimer()
    current_zoom = 1

    def setupUi(self):
        self.widget.fixed_chk.setText(locale.get("use_fixed_time_constant", "str_use_fixed_time_constant"))

        self.widget.periods_lb.setText(locale.get("period_number", "str_period_number"))
        self.widget.time_constant_lb.setText(locale.get("fixed_time_constant", "str_fixed_time_constant"))

        self.widget.start_bt.setText(locale.get("start", "str_start"))

        self.widget.progress_lb.setText(locale.get("progress", "str_progress"))
        self.widget.current_lb.setText(locale.get("current_point", "str_current_point"))

        self.widget.chart_lb.setText(locale.get("amplitude", "str_amplitude"))

        self.widget.zoom_in_bt.setText(locale.get("plus_zoom", "str_plus_zoom"))
        self.widget.zoom_out_bt.setText(locale.get("minus_zoom", "str_minus_zoom"))
        self.widget.zoom_reset_bt.setText(locale.get("reset_zoom", "str_reset_zoom"))
        self.widget.map_lb.setText(locale.get("image", "str_image"))

        self.widget.histogram_lb.setText(locale.get("histogram", "str_histogram"))

    def connect_backend(self):
        # Progress bar control
        connect_feat(self.widget.time_constant_cb, self.backend.lockin_backend().lockin, "time_constant")

        # Chart
        self.amp_chart = AmpChart(self.widget.chart_lt, self.backend)

        # Map control
        self.scene = QGraphicsScene(0, 0, 200, 200)
        self.widget.map_view.setScene(self.scene)
        self.progress_bar_controller = ProgressBarController(self.widget.exp_bar, self.widget.start_bt,
                                                             self.backend.worker,
                                                             self.widget.current_le)

        self.widget.zoom_in_bt.clicked.connect(self.view_zoom_in)
        self.widget.zoom_out_bt.clicked.connect(self.view_zoom_out)
        self.widget.zoom_reset_bt.clicked.connect(self.view_zoom_reset)

        self.view_timer.setInterval(30)
        self.view_timer.timeout.connect(self.load_points)
        self.view_timer.start()

        # Histogram
        self.phase_chart = PhaseHistogram(self.widget.histogram_vl, self.backend)

    def load_points(self):
        try:
            pixmap = QPixmap()
            pixmap.convertFromImage(self.progress_bar_controller.qimage())

            if hasattr(self, "g_pixmap"):
                self.scene.removeItem(self.g_pixmap)
            self.g_pixmap = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.g_pixmap)
        except:
            traceback.print_exc()

    def view_zoom_in(self):
        scale = 2
        self.current_zoom *= scale
        self.widget.map_view.scale(scale, scale)
        return

    def view_zoom_out(self):
        scale = 0.5
        self.current_zoom *= scale
        self.widget.map_view.scale(scale, scale)
        return

    def view_zoom_reset(self):
        self.widget.map_view.scale(1/self.current_zoom, 1/self.current_zoom)
        self.current_zoom = 1
        return