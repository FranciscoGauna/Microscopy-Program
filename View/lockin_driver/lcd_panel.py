from Drivers.Lockin.anfatec_driver import AnfatecAMU24
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLCDNumber, QComboBox, QVBoxLayout, QHBoxLayout, QLabel
from View.localization import locale


class LCDPanel:

    def __init__(self, lockin: AnfatecAMU24()):
        self.display = QLCDNumber()
        self.timer = QTimer()
        self.combo_box = self.channel_combo()
        self.lockin = lockin
        self._func_to_index = {
            self.reload_x: 0,
            self.reload_y: 1,
            self.reload_amplitude: 2,
            self.reload_phase: 3
        }

    def channel_combo(self):
        chanel_cb = QComboBox()
        chanel_cb.addItem(locale.get("X", "str_X"))
        chanel_cb.addItem(locale.get("Y", "str_Y"))
        chanel_cb.addItem(locale.get("amplitude", "str_amplitude"))
        chanel_cb.addItem(locale.get("phase", "str_phase"))
        chanel_cb.currentIndexChanged.connect(self.change_channel)
        return chanel_cb

    def build_display(self, func):
        layout = QVBoxLayout()
        upper_layout = QVBoxLayout()
        upper_layout.addStretch(0)
        under_layout = QVBoxLayout()
        channel_layout = QHBoxLayout()

        channel_layout.addWidget(QLabel(locale.get("channel", "str_channel")))
        self.combo_box.setCurrentIndex(self._func_to_index[func])
        channel_layout.addWidget(self.combo_box)

        self.display.setMinimumHeight(80)
        self.display.setDigitCount(10)
        self.timer.setInterval(2000)
        self.timer.timeout.connect(func)
        self.timer.start()
        func()

        upper_layout.addWidget(self.display)
        under_layout.addLayout(channel_layout)
        under_layout.addStretch(1)
        layout.addLayout(upper_layout)
        layout.addLayout(under_layout)
        return layout

    def change_channel(self):
        funcs = [self.reload_x, self.reload_y, self.reload_amplitude, self.reload_phase]
        funcs[self.combo_box.currentIndex()]()

        self.timer = QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(funcs[self.combo_box.currentIndex()])
        self.timer.start()

    def reload_amplitude(self):
        self.display.display(self.lockin.amplitude.magnitude)

    def reload_phase(self):
        self.display.display(self.lockin.phase.magnitude)

    def reload_x(self):
        self.display.display(self.lockin.real_part_x())

    def reload_y(self):
        self.display.display(self.lockin.imaginary_part_y())
