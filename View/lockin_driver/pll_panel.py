from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QLabel, QLineEdit, QHBoxLayout
from lantz import Q_
from View.localization import locale
from View.pyqt_utils import delete_items_of_layout


class PllPanel:
    """This class is used for building and managing a panel that interacts with the pll and lockin values, providing an
     appropriate interface for situations where the pll is on or off
     This class should be saved in a internal variable of the window, or it will get garbage collected, and the timers
     and update methods will not work"""
    def __init__(self, lockin):
        self.lockin = lockin
        self.layout = QVBoxLayout()
        self.frequency_counter = None
        self.frequency_timer = None
        self.frequency_input = None
        self.amplitude_input = None
        self.phase_input = None
        self.status_indicator = None
        self.status_timer = None

    def pll_layout(self):
        self.layout.addLayout(self.on_layout()) if self.lockin.pll else self.layout.addLayout(self.off_layout())
        return self.layout

    def set_pll(self):
        # No funciona bien, cuando se prende y se apaga
        self.lockin.pll = not self.lockin.pll

        # Borrar layout viejo
        item = self.layout.takeAt(0)
        self.frequency_timer = None
        self.frequency_counter = None
        self.frequency_input = None
        self.amplitude_input = None
        self.phase_input = None
        delete_items_of_layout(item)

        # Generar layout nuevo
        self.layout.addLayout(self.on_layout()) if self.lockin.pll else self.layout.addLayout(self.off_layout())

    def on_layout(self):
        """Creates a layout with the external frequency and an overload status for when the pll is on"""
        check_box = self.make_pll_checkbox()

        frequency_label = QLabel(locale.get("external_frequency", "str_external_frequency"))
        frequency_units = QLabel("Hz")
        frequency_units.setMaximumWidth(20)
        self.frequency_counter = QLineEdit(str(self.lockin.pll_frequency()))
        self.frequency_counter.setMaximumWidth(200)
        self.frequency_counter.setReadOnly(True)
        self.frequency_timer = QTimer()
        self.frequency_timer.setInterval(500)
        self.frequency_timer.timeout.connect(self.reload_external_frequency)
        self.frequency_timer.start()

        frequency_layout = QHBoxLayout()
        frequency_layout.addWidget(self.frequency_counter)
        frequency_layout.addWidget(frequency_units)
        upper_layout = QVBoxLayout()
        upper_layout.addStretch(0)
        upper_layout.addWidget(check_box)
        under_layout = QVBoxLayout()
        under_layout.addWidget(frequency_label)
        under_layout.addLayout(frequency_layout)
        under_layout.addWidget(self.make_status_label())

        under_layout.addStretch(1)
        on_layout = QVBoxLayout()
        on_layout.addLayout(upper_layout)
        on_layout.addLayout(under_layout)
        return on_layout

    def reload_external_frequency(self):
        """Function gets called by a timer: Updates the external frequency"""
        self.frequency_counter.setText(str(self.lockin.pll_frequency()))

    def off_layout(self):
        """Creates a layout with the external frequency and an overload status for when the pll is on"""
        check_box = self.make_pll_checkbox()

        frequency_units = QLabel("Hz")
        frequency_units.setMaximumWidth(20)
        amplitude_units = QLabel("V")
        amplitude_units.setMaximumWidth(20)
        phase_units = QLabel("º")
        phase_units.setMaximumWidth(20)
        self.frequency_input = QLineEdit(str(self.lockin.lockin_frequency.magnitude))
        self.frequency_input.editingFinished.connect(self.insert_frequency)
        self.frequency_input.setValidator(QDoubleValidator())
        self.frequency_input.setMaximumWidth(200)
        self.amplitude_input = QLineEdit(str(self.lockin.lockin_amplitude.magnitude))
        self.amplitude_input.editingFinished.connect(self.insert_amplitude)
        self.amplitude_input.setValidator(QDoubleValidator())
        self.amplitude_input.setMaximumWidth(200)
        self.phase_input = QLineEdit(str(self.lockin.lockin_phase.magnitude))
        self.phase_input.editingFinished.connect(self.insert_phase)
        self.phase_input.setValidator(QDoubleValidator())
        self.phase_input.setMaximumWidth(200)

        frequency_layout = QHBoxLayout()
        frequency_layout.addWidget(self.frequency_input)
        frequency_layout.addWidget(frequency_units)
        amplitude_layout = QHBoxLayout()
        amplitude_layout.addWidget(self.amplitude_input)
        amplitude_layout.addWidget(amplitude_units)
        phase_layout = QHBoxLayout()
        phase_layout.addWidget(self.phase_input)
        phase_layout.addWidget(phase_units)

        upper_layout = QVBoxLayout()
        upper_layout.addStretch(0)
        upper_layout.addWidget(check_box)
        under_layout = QVBoxLayout()
        upper_layout.addWidget(QLabel(locale.get("frequency_input", "str_frequency_input")))
        upper_layout.addLayout(frequency_layout)
        under_layout.addWidget(QLabel(locale.get("amplitude_input", "str_amplitude_input")))
        under_layout.addLayout(amplitude_layout)
        under_layout.addWidget(QLabel(locale.get("phase_input", "str_phase_input")))
        under_layout.addLayout(phase_layout)
        under_layout.addWidget(self.make_status_label())

        under_layout.addStretch(1)
        off_layout = QVBoxLayout()
        off_layout.addLayout(upper_layout)
        off_layout.addLayout(under_layout)
        return off_layout

    def make_pll_checkbox(self):
        check_box = QCheckBox(locale.get("external_reference", "str_external_reference"))
        check_box.setChecked(self.lockin.pll)
        check_box.stateChanged.connect(self.set_pll)
        return check_box

    def make_status_label(self):
        self.status_indicator = QLabel("")
        self.status_indicator.setStyleSheet("color: black;")
        self.status_timer = QTimer()
        self.status_timer.setInterval(1000)
        self.status_timer.timeout.connect(self.status_overload)
        self.status_timer.start()
        return self.status_indicator

    def status_overload(self):
        if self.lockin.overloaded:
            self.status_indicator.setStyleSheet("color: black; background-color: red;")
            self.status_indicator.setText(locale.get("overloaded", "str_overloaded"))
        else:
            self.status_indicator.setStyleSheet("color: black;")
            self.status_indicator.setText("")

    def insert_frequency(self):
        """Function gets called when the user inputs a value in the text box: Updates the lockin frequency"""
        self.lockin.lockin_frequency = Q_(float(self.frequency_input.text()), "hertz")

    def insert_amplitude(self):
        """Function gets called when the user inputs a value in the text box: Updates the lockin amplitude"""
        self.lockin.lockin_amplitude = Q_(float(self.amplitude_input.text()), "V")

    def insert_phase(self):
        """Function gets called when the user inputs a value in the text box: Updates the lockin phase"""
        self.lockin.lockin_phase = Q_(float(self.phase_input.text()), "deg")
