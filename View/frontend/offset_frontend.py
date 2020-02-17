from lantz.qt import Frontend

from View.frontend.camera_control_ui import ImageDrawerFt
from View.localization import locale


class OffsetFrontend(Frontend):
    gui = ("UI", "offset_control.ui")
    drawer: ImageDrawerFt

    def __init__(self, drawer):
        super().__init__()

        self.drawer = drawer
        self.widget.load_off_bt.pressed.connect(self.update_offset)

    def setupUi(self):
        self.widget.x_off_lb.setText(locale.get("y_offset", "str_y_offset"))
        self.widget.y_off_lb.setText(locale.get("y_offset", "str_y_offset"))
        self.widget.load_off_bt.setText(locale.get("load_offset", "str_load_offset"))

    def update_offset(self):
        x_o = - self.widget.x_off_sb.value()
        y_o = - self.widget.y_off_sb.value()

        self.drawer.update_offset(x_o, y_o)

