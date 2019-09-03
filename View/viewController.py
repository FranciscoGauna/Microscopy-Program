from View.localization import locale
from View.mainWidgets import make_gain_buttons, make_time_constant_box, Helper
from Model.AnfatecDriver import AnfatecAMU24
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLCDNumber
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Lockin Controller")
        self.lockin = AnfatecAMU24()
        self.helper = Helper(self.lockin)

        layout = QHBoxLayout()
        stats_layout = QVBoxLayout()
        amplitude_layout = QVBoxLayout()
        phase_layout = QVBoxLayout()
        signal_layout = QVBoxLayout()
        stats_layout.addLayout(make_time_constant_box(self))
        stats_layout.addLayout(make_gain_buttons(self))
        amplitude_layout.addLayout(self.create_amplitude_lcd_display())
        phase_layout.addLayout(self.create_phase_lcd_display())

        layout.addLayout(stats_layout)
        layout.addLayout(amplitude_layout)
        layout.addLayout(phase_layout)
        layout.addLayout(signal_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_amplitude_lcd_display(self):
        layout = QVBoxLayout()
        self.amplitude_widget = QLCDNumber(self)
        self.amplitude_timer = QTimer()
        self.amplitude_timer.setInterval(1000)
        self.amplitude_timer.timeout.connect(self.reload_amplitude)
        self.amplitude_timer.start()
        layout.addWidget(self.amplitude_widget)

        return layout

    def reload_amplitude(self):
        self.amplitude_widget.display(self.lockin.amplitude.magnitude)

    def create_phase_lcd_display(self):
        layout = QVBoxLayout()
        self.phase_widget = QLCDNumber(self)
        self.phase_timer = QTimer()
        self.phase_timer.setInterval(1000)
        self.phase_timer.timeout.connect(self.reload_phase)
        self.phase_timer.start()
        layout.addWidget(self.phase_widget)

        return layout

    def reload_phase(self):
        self.phase_widget.display(self.lockin.phase.magnitude)

