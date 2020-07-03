from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from lantz.qt import Frontend, InstrumentSlot
from lantz.qt.connect import connect_feat

from Backend.focus_backend import FocusBackend
from View.localization import locale


class FocusFrontend(Frontend):
    gui = ("UI", "focus_control.ui")
    backend: FocusBackend

    def setupUi(self):
        self.widget.control_focus_cb.setText(locale.get("control_focus", "str_control_focus"))

        self.widget.fc_current_lb.setText(locale.get("fc_current_percent", "str_fc_current_percent"))
        self.widget.fc_current_cb.setText(locale.get("on_off", "str_on_off"))

        self.widget.probe_current_lb.setText(locale.get("probe_current_percent", "str_probe_current_percent"))
        self.widget.probe_current_cb.setText(locale.get("on_off", "str_on_off"))

        self.widget.efocus_chart_lb.setText(locale.get("efocus", "str_efocus"))
        self.widget.sum_chart_lb.setText(locale.get("sum", "str_sum"))
        self.widget.reflectance_chart_lb.setText(locale.get("reflectance", "str_reflectance"))

        self.widget.focus_light_status.setText(locale.get("focus", "str_focus"))
        self.widget.focus_light_status.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.widget.focus_light_status.setFocusPolicy(Qt.NoFocus)

    def connect_backend(self):

        connect_feat(self.widget.focus_light_status, self.backend, "focus_status")

        series = QLineSeries()
        series.setName(locale.get("amplitude_mv", "str_amplitude_mv"))
        series.append(0, 1)
        series.append(1, 1)
        chart = QChart(flags=Qt.WindowFlags())
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart_view = QChartView()
        chart_view.setChart(chart)
        self.widget.efocus_chart_lt.addWidget(chart_view)

        series = QLineSeries()
        series.setName(locale.get("amplitude_mv", "str_amplitude_mv"))
        series.append(0, 1)
        series.append(1, 1)
        chart = QChart(flags=Qt.WindowFlags())
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart_view = QChartView()
        chart_view.setChart(chart)
        self.widget.sum_chart_lt.addWidget(chart_view)

        series = QLineSeries()
        series.setName(locale.get("amplitude_mv", "str_amplitude_mv"))
        series.append(0, 1)
        series.append(1, 1)
        chart = QChart(flags=Qt.WindowFlags())
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart_view = QChartView()
        chart_view.setChart(chart)
        self.widget.reflectance_chart_lt.addWidget(chart_view)
