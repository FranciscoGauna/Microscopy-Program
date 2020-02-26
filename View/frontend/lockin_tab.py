import math
from datetime import datetime

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from lantz.qt import Frontend
from PyQt5.QtChart import QLineSeries, QChart, QChartView, QValueAxis

from Backend.lockin_options import LockinBackend
from View.frontend.lockin_options import LockinOptions
from View.frontend.lockin_pll import LockinPll
from View.localization import locale
from magic_numbers import max_point_chart, chart_volt_resolution


class LockinTab(Frontend):
    gui = ("UI", "lockin_tab.ui")
    backend: LockinBackend

    timer: QTimer
    start_time: datetime

    amp_chart: QChart
    amp_chart_view: QChartView
    amp_series: QLineSeries
    amp_y_max: float
    amp_y_min: float
    amp_y_axe: QValueAxis

    phase_chart: QChart
    phase_chart_view: QChartView
    phase_series: QLineSeries
    phase_y_max: float
    phase_y_min: float
    phase_y_axe: QValueAxis

    real_chart: QChart
    real_chart_view: QChartView
    real_series: QLineSeries
    real_y_max: float
    real_y_min: float
    real_y_axe: QValueAxis

    imag_chart: QChart
    imag_chart_view: QChartView
    imag_series: QLineSeries
    imag_y_max: float
    imag_y_min: float
    imag_y_axe: QValueAxis

    lockin_options: LockinOptions
    lockin_pll: LockinPll

    def setupUi(self):
        self.widget.amp_cb.setText(locale.get("auto_limits", "str_auto_limits"))
        self.widget.phase_cb.setText(locale.get("auto_limits", "str_auto_limits"))
        self.widget.real_cb.setText(locale.get("auto_limits", "str_auto_limits"))
        self.widget.imag_cb.setText(locale.get("auto_limits", "str_auto_limits"))

    def connect_backend(self):
        self.lockin_options = LockinOptions(backend=self.backend)
        self.lockin_pll = LockinPll(backend=self.backend)

        self.widget.top_lt.addWidget(self.lockin_options)
        self.widget.top_lt.addWidget(self.lockin_pll)

        self.amp_series = QLineSeries()
        self.amp_series.setName(locale.get("amplitude", "str_amplitude"))
        self.amp_y_max = 0.01
        self.amp_y_min = 0

        self.amp_chart = QChart(flags=Qt.WindowFlags())
        self.amp_chart.addSeries(self.amp_series)
        self.amp_chart.createDefaultAxes()
        self.amp_y_axe = self.amp_chart.axes(Qt.Vertical)[0]
        self.amp_chart_view = QChartView()
        self.amp_chart_view.setRenderHint(QPainter.Antialiasing)
        self.amp_chart_view.setChart(self.amp_chart)

        self.phase_series = QLineSeries()
        self.phase_series.setName(locale.get("phase", "str_phase"))
        self.phase_y_max = 180
        self.phase_y_min = -180

        self.phase_chart = QChart(flags=Qt.WindowFlags())
        self.phase_chart.addSeries(self.phase_series)
        self.phase_chart.createDefaultAxes()
        self.phase_y_axe = self.phase_chart.axes(Qt.Vertical)[0]
        self.phase_chart_view = QChartView()
        self.phase_chart_view.setRenderHint(QPainter.Antialiasing)
        self.phase_chart_view.setChart(self.phase_chart)

        self.real_series = QLineSeries()
        self.real_series.setName(locale.get("real_part", "str_real_part"))
        self.real_y_max = 0.01
        self.real_y_min = 0

        self.real_chart = QChart(flags=Qt.WindowFlags())
        self.real_chart.addSeries(self.real_series)
        self.real_chart.createDefaultAxes()
        self.real_y_axe = self.real_chart.axes(Qt.Vertical)[0]
        self.real_chart_view = QChartView()
        self.real_chart_view.setRenderHint(QPainter.Antialiasing)
        self.real_chart_view.setChart(self.real_chart)

        self.imag_series = QLineSeries()
        self.imag_series.setName(locale.get("imaginary_part", "str_imaginary_part"))
        self.imag_y_max = 0.01
        self.imag_y_min = 0

        self.imag_chart = QChart(flags=Qt.WindowFlags())
        self.imag_chart.addSeries(self.imag_series)
        self.imag_chart.createDefaultAxes()
        self.imag_y_axe = self.imag_chart.axes(Qt.Vertical)[0]
        self.imag_chart_view = QChartView()
        self.imag_chart_view.setRenderHint(QPainter.Antialiasing)
        self.imag_chart_view.setChart(self.imag_chart)

        self.widget.bot_lt.addWidget(self.amp_chart_view, 1, 0)
        self.widget.bot_lt.addWidget(self.phase_chart_view, 1, 1)
        self.widget.bot_lt.addWidget(self.real_chart_view, 1, 2)
        self.widget.bot_lt.addWidget(self.imag_chart_view, 1, 3)

        self.start_time = datetime.now()
        self.timer = QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.expand_line_series)
        self.timer.start()

    def expand_line_series(self):
        x = (datetime.now() - self.start_time).total_seconds()

        amp_point = None
        y = self.backend.get_amplitude() * chart_volt_resolution
        if self.amp_series.count() > max_point_chart:
            amp_point = self.amp_series.at(0)
            self.amp_series.remove(0)
        if self.widget.amp_cb.isChecked():
            if amp_point is not None and amp_point.y() == self.amp_y_max:
                self.amp_y_max = find_max_series(self.amp_series)
            elif amp_point is not None and amp_point.y() == self.amp_y_min:
                self.amp_y_min = find_min_series(self.amp_series)
            if y > self.amp_y_max:
                self.amp_y_max = y
            elif y < self.amp_y_min:
                self.amp_y_min = y
            self.widget.amp_max_sb.setValue(self.amp_y_max)
            self.widget.amp_min_sb.setValue(self.amp_y_min)
        else:
            self.amp_y_max = self.widget.amp_max_sb.value()
            self.amp_y_min = self.widget.amp_min_sb.value()
        self.amp_series.append(x, y)
        axe = self.amp_chart.axes(Qt.Horizontal)[0]
        axe.setRange(self.amp_series.at(0).x(), self.amp_series.at(len(self.amp_series) - 1).x())
        self.amp_y_axe.setRange(self.amp_y_min, self.amp_y_max)
        self.amp_chart_view.repaint()

        y = self.backend.get_phase()
        self.phase_series.append(x, y)
        if self.phase_series.count() > max_point_chart:
            self.phase_series.remove(0)
        axe = self.phase_chart.axes(Qt.Horizontal)[0]
        axe.setRange(self.phase_series.at(0).x(), self.phase_series.at(len(self.phase_series) - 1).x())
        self.phase_y_axe.setRange(self.phase_y_min, self.phase_y_max)
        self.phase_chart_view.repaint()

        y = self.backend.get_real_part() * chart_volt_resolution
        if y > self.real_y_max:
            self.real_y_max = y
        elif y < self.real_y_min:
            self.real_y_min = y
        self.real_series.append(x, y)
        if self.real_series.count() > max_point_chart:
            self.real_series.remove(0)
        axe = self.real_chart.axes(Qt.Horizontal)[0]
        axe.setRange(self.real_series.at(0).x(), self.real_series.at(len(self.real_series) - 1).x())
        self.real_y_axe.setRange(self.real_y_min, self.real_y_max)
        self.real_chart_view.repaint()

        y = self.backend.get_imaginary_part() * chart_volt_resolution
        if y > self.imag_y_max:
            self.imag_y_max = y
        elif y < self.imag_y_min:
            self.imag_y_min = y
        self.imag_series.append(x, y)
        if self.imag_series.count() > max_point_chart:
            self.imag_series.remove(0)
        axe = self.imag_chart.axes(Qt.Horizontal)[0]
        axe.setRange(self.imag_series.at(0).x(), self.imag_series.at(len(self.imag_series) - 1).x())
        self.imag_y_axe.setRange(self.imag_y_min, self.imag_y_max)
        self.imag_chart_view.repaint()


def find_max_series(serie):
    result = -math.inf
    for element in serie:
        if element.y() > result:
            result = element.y()
    return result


def find_min_series(serie):
    result = math.inf
    for element in serie:
        if element.y() < result:
            result = element.y()
    return result
