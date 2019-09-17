from View.lockin_driver.option_panel import OptionsPanel
from Model.AnfatecDriver import AnfatecAMU24
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from View.lockin_driver.lcd_panel import LCDPanel
from View.lockin_driver.pll_panel import PllPanel
"""Main windows for the program"""

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Lockin Controller")
        self.lockin = AnfatecAMU24()
        self.helper = OptionsPanel(self.lockin)
        self.amplitude_display = LCDPanel(self.lockin)
        self.phase_display = LCDPanel(self.lockin)
        self.pll_tab = PllPanel(self.lockin)

        layout = QHBoxLayout()
        stats_layout = self.helper.make_layout()
        amplitude_layout = QVBoxLayout()
        phase_layout = QVBoxLayout()
        signal_layout = self.pll_tab.pll_layout()
        amplitude_layout.addLayout(self.amplitude_display.build_display(self.amplitude_display.reload_amplitude))
        phase_layout.addLayout(self.phase_display.build_display(self.phase_display.reload_phase))

        layout.addLayout(stats_layout)
        layout.addLayout(amplitude_layout)
        layout.addLayout(phase_layout)
        layout.addLayout(signal_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

