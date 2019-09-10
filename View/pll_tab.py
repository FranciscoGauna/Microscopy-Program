from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QLabel, QLineEdit, QSpacerItem, QHBoxLayout
from lantz import Q_
from View.localization import locale


class PllTab:
    def __init__(self, lockin):
        self.lockin = lockin
        self.layout = QVBoxLayout()
        self.frequency_counter = None
        self.frequency_timer = None
        self.frequency_input = None
        self.amplitude_input = None
        self.phase_input = None

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
        check_box = QCheckBox(locale.get("external_reference", "str_external_reference"))
        check_box.setChecked(self.lockin.pll)
        check_box.stateChanged.connect(self.set_pll)

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

        under_layout.addStretch(1)
        on_layout = QVBoxLayout()
        on_layout.addLayout(upper_layout)
        on_layout.addLayout(under_layout)
        return on_layout

    def reload_external_frequency(self):
        self.frequency_counter.setText(str(self.lockin.pll_frequency()))

    def off_layout(self):
        check_box = QCheckBox(locale.get("external_reference", "str_external_reference"))
        check_box.setChecked(self.lockin.pll)
        check_box.stateChanged.connect(self.set_pll)

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

        under_layout.addStretch(1)
        off_layout = QVBoxLayout()
        off_layout.addLayout(upper_layout)
        off_layout.addLayout(under_layout)
        return off_layout

    def insert_frequency(self):
        self.lockin.lockin_frequency = Q_(float(self.frequency_input.text()), "hertz")

    def insert_amplitude(self):
        self.lockin.lockin_amplitude = Q_(float(self.amplitude_input.text()), "V")

    def insert_phase(self):
        self.lockin.lockin_phase = Q_(float(self.phase_input.text()), "deg")


# Refactor, it should be a top level utility function
def delete_items_of_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if isinstance(item, QSpacerItem):
                pass
            elif widget is not None:
                widget.deleteLater()
            else:
                delete_items_of_layout(item.layout())
