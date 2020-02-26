from lantz.qt import Frontend

from View.localization import locale


class OffsetFrontend(Frontend):
    gui = ("UI", "offset_control.ui")

    def __init__(self, drawer):
        super().__init__()

        self.drawer = drawer
        self.drawer.offset_ft = self
        self.widget.load_off_bt.pressed.connect(self.update_offset)
        self.widget.click_off_cb.clicked.connect(self.toggle_drawer_click)

    def setupUi(self):
        self.widget.x_off_lb.setText(locale.get("y_offset", "str_y_offset"))
        self.widget.y_off_lb.setText(locale.get("y_offset", "str_y_offset"))
        self.widget.load_off_bt.setText(locale.get("load_offset", "str_load_offset"))

    def update_offset(self):
        x_o = - self.widget.x_off_sb.value()
        y_o = - self.widget.y_off_sb.value()

        self.drawer.update_offset(x_o, y_o)

    def set_offset(self, x, y):
        self.widget.x_off_sb.setValue(x)
        self.widget.y_off_sb.setValue(y)
        self.update_offset()

    def toggle_drawer_click(self):
        self.drawer.flag_click_override = not self.drawer.flag_click_override
