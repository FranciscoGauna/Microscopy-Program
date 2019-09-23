from lantz.qt import Frontend
from Backend.lockin_options_backend import LockinControl
from View.frontend.lockin_display import LockinDisplay
from View.frontend.lockin_options import LockinOptions


class LockinControlUi(Frontend):
    backend: LockinControl
    gui = ('frontend', 'UI', 'lockin_window.ui')

    def connect_backend(self):
        super().connect_backend()
        self.options = LockinOptions(backend=self.backend)
        self.amplitude_display = LockinDisplay(0, backend=self.backend)
        self.phase_display = LockinDisplay(1, backend=self.backend)
        self.options_layout.addWidget(self.options.widget)
        self.amplitude_layout.addWidget(self.amplitude_display.widget)
        self.phase_layout.addWidget(self.phase_display.widget)
