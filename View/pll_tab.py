from PyQt5.QtWidgets import QVBoxLayout, QCheckBox


class PllTab:
    def __init__(self, lockin):
        self.lockin = lockin

    def pll_layout(self):
        self.layout = QVBoxLayout()
        check_box = QCheckBox("External Reference")
        check_box.setChecked(self.lockin.pll)
        check_box.stateChanged.connect(self.set_pll)
        self.layout.addWidget(check_box)
        return self.layout

    def set_pll(self):
        self.lockin.pll = not self.lockin.pll
