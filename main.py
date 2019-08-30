from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Model.AnfatecDriver import AnfatecAMU24

class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Lockin Controller")
        self.lockin = AnfatecAMU24()

        layout = QHBoxLayout()

        stats_layout = QVBoxLayout()
        amplitude_layout = QVBoxLayout()
        phase_layout = QVBoxLayout()
        signal_layout = QVBoxLayout()
        stats_layout.addWidget(Color('red'))
        amplitude_layout.addWidget(self._create_amplitude_lcd_display())
        phase_layout.addWidget(self._create_phase_lcd_display())
        signal_layout.addWidget(Color('blue'))

        layout.addLayout(self._gain_buttons())
        layout.addLayout(amplitude_layout)
        layout.addLayout(phase_layout)
        layout.addLayout(signal_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _create_amplitude_lcd_display(self):
        self.amplitude_widget = QLCDNumber(self)

        self.amplitude_timer = QTimer()
        self.amplitude_timer.setInterval(1000)
        self.amplitude_timer.timeout.connect(self._reload_amplitude)
        self.amplitude_timer.start()

        return self.amplitude_widget

    def _reload_amplitude(self):
        self.amplitude_widget.display(self.lockin.amplitude.magnitude)

    def _create_phase_lcd_display(self):
        self.phase_widget = QLCDNumber(self)

        self.phase_timer = QTimer()
        self.phase_timer.setInterval(1000)
        self.phase_timer.timeout.connect(self._reload_phase)
        self.phase_timer.start()

        return self.phase_widget

    def _reload_phase(self):
        self.phase_widget.display(self.lockin.phase.magnitude)

    def _gain_buttons(self):
        parent_layout = QVBoxLayout()  # layout for the central widget
        layout = QVBoxLayout()  # layout for the central widget
        widget = QWidget(self)  # central widget
        widget.setLayout(layout)

        number_group = QButtonGroup(widget)  # Number group
        r0 = QRadioButton("0")
        r0.pressed.connect(self._test_func)
        number_group.addButton(r0)
        r1 = QRadioButton("1")
        number_group.addButton(r1)
        r2 = QRadioButton("2")
        number_group.addButton(r2)
        layout.addWidget(r0)
        layout.addWidget(r1)
        layout.addWidget(r2)
        parent_layout.addWidget(widget)
        return parent_layout

    def _test_func(self):
        print("All Good!")


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
