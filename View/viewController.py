from View.mainWidgets import make_gain_buttons, make_time_constant_box, Helper
from Model.AnfatecDriver import AnfatecAMU24
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget

from View.pll_tab import PllTab


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Lockin Controller")
        self.lockin = AnfatecAMU24()
        self.helper = Helper(self.lockin)
        self.pll_tab = PllTab(self.lockin)

        layout = QHBoxLayout()
        stats_layout = QVBoxLayout()
        amplitude_layout = QVBoxLayout()
        phase_layout = QVBoxLayout()
        signal_layout = self.pll_tab.pll_layout()
        stats_layout.addLayout(make_time_constant_box(self))
        stats_layout.addLayout(make_gain_buttons(self))
        amplitude_layout.addLayout(self.helper.create_amplitude_lcd_display(self))
        phase_layout.addLayout(self.helper.create_phase_lcd_display(self))

        layout.addLayout(stats_layout)
        layout.addLayout(amplitude_layout)
        layout.addLayout(phase_layout)
        layout.addLayout(signal_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

