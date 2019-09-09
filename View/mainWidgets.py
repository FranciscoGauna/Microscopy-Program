from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QButtonGroup, QRadioButton, QComboBox, QLCDNumber, QHBoxLayout
from View.localization import locale


def make_gain_buttons(MainWindow):
    parent_layout = QVBoxLayout()
    parent_layout.addWidget(QLabel(locale.get("box_gain", "str_box_gain")))
    layout = QVBoxLayout()
    widget = QWidget()  # central widget
    widget.setLayout(layout)

    number_group = QButtonGroup(widget)  # Number group
    r0 = QRadioButton(locale.get("high_reserve", "str_high_reserve"))
    r0.pressed.connect(MainWindow.helper.set_high_gain)
    number_group.addButton(r0)
    r1 = QRadioButton(locale.get("normal", "str_normal"))
    r1.pressed.connect(MainWindow.helper.set_medium_gain)
    number_group.addButton(r1)
    r2 = QRadioButton(locale.get("low_noise", "str_low_noise"))
    r2.pressed.connect(MainWindow.helper.set_low_gain)
    if MainWindow.lockin.input_gain == 1:
        r0.setChecked(True)
    elif MainWindow.lockin.input_gain == 10:
        r1.setChecked(True)
    else:
        r2.setChecked(True)
    number_group.addButton(r2)
    layout.addWidget(r0)
    layout.addWidget(r1)
    layout.addWidget(r2)
    parent_layout.addWidget(widget)
    parent_layout.addStretch(1)
    return parent_layout


def make_time_constant_box(MainWindow):
    parent_layout = QVBoxLayout()
    parent_layout.addStretch(0)
    parent_layout.addWidget(QLabel(locale.get("time_constant", "str_time_constant")))
    time_constant_box = QComboBox()
    time_constant_box.addItem("0.25 ms")
    time_constant_box.addItem("0.5 ms")
    time_constant_box.addItem("1 ms")
    time_constant_box.addItem("2 ms")
    time_constant_box.addItem("5 ms")
    time_constant_box.addItem("10 ms")
    time_constant_box.addItem("20 ms")
    time_constant_box.addItem("50 ms")
    time_constant_box.addItem("0.1 s")
    time_constant_box.addItem("0.2 s")
    time_constant_box.addItem("0.5 s")
    time_constant_box.addItem("1 s")
    time_constant_box.addItem("2 s")
    time_constant_box.addItem("5 s")
    time_constant_box.currentIndexChanged.connect(MainWindow.helper.change_time_constant)
    parent_layout.addWidget(time_constant_box)
    MainWindow.helper.time_constant_box = time_constant_box
    return parent_layout


class Helper:
    def __init__(self, lockin):
        self.lockin = lockin
        self.time_constant_box = None

    def set_high_gain(self):
        self.lockin.input_gain = 1

    def set_medium_gain(self):
        self.lockin.input_gain = 10

    def set_low_gain(self):
        self.lockin.input_gain = 100

    def change_time_constant(self):
        # Este codigo usa el index y la variable times para convertir a en b
        times = [20, 20, 20, 20, 20, 20, 20, 50, 100, 200, 500, 1000, 2000, 5000]
        self.lockin.set_lockin_time_constant(self.time_constant_box.currentIndex())
        self.amplitude_timer.setInterval(10*times[self.time_constant_box.currentIndex()])
        self.phase_timer.setInterval(10*times[self.time_constant_box.currentIndex()])

    def channel_combo(self):
        chanel_cb = QComboBox()
        chanel_cb.addItem(locale.get("X", "str_X"))
        chanel_cb.addItem(locale.get("Y", "str_Y"))
        chanel_cb.addItem(locale.get("amplitude", "str_amplitude"))
        chanel_cb.addItem(locale.get("phase", "str_phase"))
        return chanel_cb

    def create_amplitude_lcd_display(self, MainWindow):
        layout = QVBoxLayout()
        upper_layout = QVBoxLayout()
        upper_layout.addStretch(0)
        under_layout = QVBoxLayout()
        channel_layout = QHBoxLayout()

        channel_layout.addWidget(QLabel(locale.get("channel", "str_channel")))
        channel_cb = self.channel_combo()
        channel_cb.setCurrentIndex(2)
        channel_layout.addWidget(channel_cb)

        self.amplitude_widget = QLCDNumber(MainWindow)
        self.amplitude_widget.setMinimumHeight(80)
        self.amplitude_timer = QTimer()
        self.amplitude_timer.setInterval(1000)
        self.amplitude_timer.timeout.connect(self.reload_amplitude)
        self.amplitude_timer.start()

        upper_layout.addWidget(self.amplitude_widget)
        under_layout.addLayout(channel_layout)
        under_layout.addStretch(1)
        layout.addLayout(upper_layout)
        layout.addLayout(under_layout)
        return layout

    def reload_amplitude(self):
        self.amplitude_widget.display(self.lockin.amplitude.magnitude)

    def create_phase_lcd_display(self, MainWindow):
        layout = QVBoxLayout()
        upper_layout = QVBoxLayout()
        upper_layout.addStretch(0)
        under_layout = QVBoxLayout()
        channel_layout = QHBoxLayout()

        channel_layout.addWidget(QLabel(locale.get("channel", "str_channel")))
        channel_cb = self.channel_combo()
        channel_cb.setCurrentIndex(3)
        channel_layout.addWidget(channel_cb)

        self.phase_widget = QLCDNumber(MainWindow)
        self.phase_widget.setMinimumHeight(80)
        self.phase_timer = QTimer()
        self.phase_timer.setInterval(1000)
        self.phase_timer.timeout.connect(self.reload_phase)
        self.phase_timer.start()

        upper_layout.addWidget(self.phase_widget)
        under_layout.addLayout(channel_layout)
        under_layout.addStretch(1)
        layout.addLayout(upper_layout)
        layout.addLayout(under_layout)
        return layout

    def reload_phase(self):
        self.phase_widget.display(self.lockin.phase.magnitude)
