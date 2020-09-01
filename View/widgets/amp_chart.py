import traceback
from math import floor

from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QBarSeries, QBarSet, QBarCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from Backend.lockin_backend import LockinBackend
from View.localization import locale

max_points = 1000

def get_list(results):
    length = len(results)
    series = []
    if length > max_points:
        series = results[-max_points:]
    else:
        for i in range(length):
            series.append(results[i])
    return series


class AmpChart(QWidget):
    chart: QChart
    chart_view: QChartView
    series: QLineSeries
    x_axe: QValueAxis
    y_axe: QValueAxis
    lockin_be: LockinBackend
    timer = QTimer()

    def __init__(self, child_layout: QVBoxLayout, backend):
        super().__init__()

        self.series = QLineSeries()
        self.series.setName(locale.get("amplitude_mv", "str_amplitude_mv"))

        self.chart = QChart(flags=Qt.WindowFlags())
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.x_axe = self.chart.axes(Qt.Horizontal)[0]
        self.y_axe = self.chart.axes(Qt.Vertical)[0]
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setChart(self.chart)

        child_layout.addWidget(self.chart_view)
        self.backend = backend
        self.timer.timeout.connect(self.reload_chart)
        self.timer.setInterval(30)
        self.timer.start()

    def reload_chart(self):
        try:
            new_list = get_list(self.backend.results())
            new_points = []
            max_v = None
            min_v = None
            for point in new_list:
                new_points.append(QPointF(point.time.total_seconds(), point.value))
                if max_v is None or max_v < point.value:
                    max_v = point.value
                if min_v is None or min_v > point.value:
                    min_v = point.value
            self.series.replace(new_points)
            if len(new_points) > 1:
                self.x_axe.setRange(new_points[0].x(), new_points[-1].x())
                self.y_axe.setRange(min_v, max_v)
        except:
            traceback.print_exc()


class PhaseHistogram(QWidget):
    results: list
    chart: QChart
    chart_view: QChartView
    series: QBarSeries
    y_max: float
    y_min: float
    y_axe: QValueAxis
    timer = QTimer()

    def __init__(self, child_layout: QVBoxLayout, backend):
        super().__init__()

        self.series = QBarSeries()

        self.bar_set = QBarSet(locale.get("phase", "str_phase"))
        category_set = self.init_bar_set()

        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(category_set)
        self.axis_y = QValueAxis()
        self.y_max = 1
        self.axis_y.setRange(0, self.y_max)

        self.series.append(self.bar_set)

        self.chart = QChart(flags=Qt.WindowFlags())
        self.chart.addSeries(self.series)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)
        self.y_axe = self.chart.axes(Qt.Vertical)[0]
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setChart(self.chart)

        child_layout.addWidget(self.chart_view)
        self.backend = backend
        self.result_index = 0
        self.timer.timeout.connect(self.reload_chart)
        self.timer.setInterval(30)
        self.timer.start()

    def init_bar_set(self):
        categories = []
        for i in range(0, 100):
            self.bar_set.insert(i, 0)
            categories.append(str(i))
        return categories

    def reload_chart(self):
        results = self.backend.results()
        try:
            amount = len(results)
            if amount < self.result_index:  # Restarts the bar
                self.result_index = 0
                for i in range(-181, 180):
                    self.bar_set.replace(i, 0)
            if self.result_index < amount:
                for i in range(self.result_index-1, amount):
                    new_bar = self.bar_set.at(int(floor(results[i].phase))) + 1
                    self.bar_set.replace(int(floor(results[i].phase)), new_bar)
                    if new_bar > self.y_max:
                        self.y_max += 1
                        self.y_axe.setRange(0, self.y_max)

                self.result_index = amount
        except:
            traceback.print_exc()


