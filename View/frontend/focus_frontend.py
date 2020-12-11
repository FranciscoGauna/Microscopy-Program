from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from lantz.qt import Frontend, InstrumentSlot
from lantz.qt.connect import connect_feat

from Backend.focus_backend import FocusBackend
from View.localization import locale

class FocusFrontend(Frontend):
    gui = ("UI", "focus_control.ui")
    backend: FocusBackend

    def __init__(self, main_window, backend=None):
        super().__init__(backend=backend)
        self.main_window = main_window

    def setupUi(self):
        self.widget.control_focus_cb.setText(locale.get("control_focus", "str_control_focus"))
        self.widget.fc_current_lb.setText(locale.get("fc_current_percent", "str_fc_current_percent"))
        self.widget.fc_current_cb.setText(locale.get("on_off", "str_on_off"))

        self.widget.probe_current_lb.setText(locale.get("probe_current_percent", "str_probe_current_percent"))
        self.widget.probe_current_cb.setText(locale.get("on_off", "str_on_off"))

        self.widget.efocus_chart_lb.setText(locale.get("efocus", "str_efocus"))
        self.widget.sum_chart_lb.setText(locale.get("sum", "str_sum"))
        self.widget.reflectance_chart_lb.setText(locale.get("reflectance", "str_reflectance"))

        self.widget.min_sum_lb.setText(locale.get("min_sum", "str_min_sum"))
        self.widget.z_focus_lb.setText(locale.get("z_focus", "str_z_focus"))
        self.widget.dn_lb.setText(locale.get("dn", "str_dn"))
        self.widget.range_lb.setText(locale.get("range", "str_range"))

        self.widget.offset_sum_lb.setText(locale.get("offset_sum_fe", "str_offset_sum_fe"))
        self.widget.shutdown_cb.setText(locale.get("shutdown_on_end", "str_shutdown_on_end"))
        self.widget.enable_cb.setText(locale.get("enable", "str_enable"))
        self.widget.stop_button.setText(locale.get("stop", "str_stop"))
        self.widget.speed_2_lb.setText(locale.get("speed_2", "str_speed_2"))

        self.widget.focus_light_status.setText(locale.get("focus", "str_focus"))
        self.widget.focus_light_status.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.widget.focus_light_status.setFocusPolicy(Qt.NoFocus)

    def connect_backend(self):

        self.backend.set_widget(self.widget.focus_light_status)

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

    def closeEvent(self, event):
        if not self.main_window.is_closing:
            self.main_window.close()
        event.accept()

