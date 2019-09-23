from lantz.qt import Frontend
from PyQt5.QtCore import QTimer
from Backend.lockin_options_backend import LockinControl
from View.localization import locale

class LockinDisplay(Frontend):
    backend: LockinControl
    gui = ('UI', 'lockin_display.ui')
    timer = QTimer()
    func = None
    channels = []
    starting_channel = 0

    def __init__(self, channel, *args, **kwargs):
        if channel not in range(0, 4):
            channel = 0
        self.starting_channel = channel
        super().__init__(*args, **kwargs)

    def setupUi(self):
        self.widget.display_cb.addItem(locale.get("amplitude", "str_amplitude"))
        self.widget.display_cb.addItem(locale.get("phase", "str_phase"))
        self.widget.display_cb.addItem(locale.get("X", "str_X"))
        self.widget.display_cb.addItem(locale.get("Y", "str_Y"))
        self.widget.display_cb.setCurrentIndex(self.starting_channel)
        self.widget.display_cb.currentIndexChanged.connect(self.update_channel)
        super().setupUi()

    def connect_backend(self):
        super().connect_backend()
        self.channels = [
            self.backend.get_amplitude,
            self.backend.get_phase,
            self.backend.get_real_part,
            self.backend.get_imaginary_part
        ]
        self.func = self.channels[self.starting_channel]
        self.update_lcd()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.update_lcd)
        self.timer.start()

    def update_channel(self):
        self.func = self.channels[self.widget.display_cb.currentIndex()]

    def update_lcd(self):
        self.widget.display_lcd.display(self.func())
