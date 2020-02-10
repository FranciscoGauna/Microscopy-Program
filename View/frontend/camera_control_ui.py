import cv2
from lantz.qt import Frontend
from lantz.qt.connect import connect_feat
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage

from View.frontend.camera_only import CameraOnlyWindow
from View.localization import locale
from View.frontend.point_list import PointList
from View.frontend.FrequencyStepFrontend import FrequencyStepFrontend
from View.frontend.platina_frontend import PlatinaFrontend
from View.widgets.custom_image import ImageWidget
from Backend.camera_backend import CameraBackend
from Backend.rect_backend import RectangleController
from Backend.points_backend import PointController
from Backend.lines_backend import LineController
from Backend.frequency_backend import FrequencyController
from Backend.platina_backend import PlatinaBackend
from Model.MotorDriver import Motor


class ImageDrawerFt(Frontend):
    gui = ('UI', 'camera_control.ui')
    old_paint_event = None
    flag_first_line = False
    flag_first_rect = False
    point_list_frontend: PointList
    image: ImageWidget
    frequency_frontend: FrequencyStepFrontend
    point_controller: PointController
    line_controller: LineController
    rect_controller: RectangleController

    def __init__(self, point_list, frequency_frontend, image, *args, **kwargs):
        self.point_list_frontend = point_list
        self.frequency_frontend = frequency_frontend
        self.image = image
        super().__init__(*args, **kwargs)

    def setupUi(self):
        self.widget.draw_tabs.setTabText(0, locale.get("point", "str_point"))
        self.widget.draw_tabs.setTabText(1, locale.get("line", "str_line"))
        self.widget.draw_tabs.setTabText(2, locale.get("rect", "str_rect"))

        self.widget.x_point_label.setText(locale.get("x", "str_x"))
        self.widget.y_point_label.setText(locale.get("y", "str_y"))
        self.widget.draw_point_button.setText(locale.get("draw_point", "str_draw_point"))
        self.widget.add_point_button.setText(locale.get("add_point", "str_add_point"))

        self.widget.x_start_line_label.setText(locale.get("start_x", "str_start_x"))
        self.widget.x_end_line_label.setText(locale.get("end_x", "str_end_x"))
        self.widget.y_start_line_label.setText(locale.get("start_y", "str_start_y"))
        self.widget.y_end_line_label.setText(locale.get("end_y", "str_end_y"))
        self.widget.lines_steps_label.setText(locale.get("line_steps", "str_line_steps"))
        self.widget.draw_line_button.setText(locale.get("draw_line", "str_draw_line"))
        self.widget.add_line_button.setText(locale.get("add_line", "str_add_line"))

        self.widget.x_start_rect_label.setText(locale.get("start_x", "str_start_x"))
        self.widget.x_end_rect_label.setText(locale.get("end_x", "str_end_x"))
        self.widget.y_start_rect_label.setText(locale.get("start_y", "str_start_y"))
        self.widget.y_end_rect_label.setText(locale.get("end_y", "str_end_y"))
        self.widget.x_steps_label.setText(locale.get("x_steps", "str_x_steps"))
        self.widget.y_steps_label.setText(locale.get("y_steps", "str_y_steps"))
        self.widget.draw_rect_button.setText(locale.get("draw_rect", "str_draw_rect"))
        self.widget.add_rect_button.setText(locale.get("add_rect", "str_add_rect"))

        self.connect_backend()

    def connect_backend(self):
        freq_backend = self.frequency_frontend.backend

        self.frequency_frontend.widget.oper_order_cb.currentIndexChanged.connect(self.point_list_frontend.update_view_point)
        self.point_controller = PointController(freq_backend)
        self.line_controller = LineController(freq_backend)
        self.rect_controller = RectangleController(freq_backend)

        self.image.mousePressEvent = self.get_pos

        self.widget.draw_point_button.pressed.connect(self.draw_point)
        connect_feat(self.widget.x_point_input, self.point_controller, "x")
        connect_feat(self.widget.y_point_input, self.point_controller, "y")
        self.widget.add_point_button.pressed.connect(lambda: self.point_controller.add_point(self.point_list_frontend.point_list))
        self.widget.add_point_button.pressed.connect(self.point_list_frontend.update_view_point)

        self.widget.draw_line_button.pressed.connect(self.draw_line)
        connect_feat(self.widget.x_start_line_input, self.line_controller, "x_start")
        connect_feat(self.widget.x_end_line_input, self.line_controller, "x_end")
        connect_feat(self.widget.y_start_line_input, self.line_controller, "y_start")
        connect_feat(self.widget.y_end_line_input, self.line_controller, "y_end")
        connect_feat(self.widget.lines_steps_input, self.line_controller, "line_steps")
        self.widget.add_line_button.pressed.connect(lambda: self.line_controller.add_line(self.point_list_frontend.point_list))
        self.widget.add_line_button.pressed.connect(self.point_list_frontend.update_view_point)

        self.widget.draw_rect_button.pressed.connect(self.draw_rectangle)
        connect_feat(self.widget.x_start_rect_input, self.rect_controller, "x_start")
        connect_feat(self.widget.x_end_rect_input, self.rect_controller, "x_end")
        connect_feat(self.widget.y_start_rect_input, self.rect_controller, "y_start")
        connect_feat(self.widget.y_end_rect_input, self.rect_controller, "y_end")
        connect_feat(self.widget.x_steps_input, self.rect_controller, "x_steps")
        connect_feat(self.widget.y_steps_input, self.rect_controller, "y_steps")
        self.widget.add_rect_button.pressed.connect(lambda: self.rect_controller.add_rect(self.point_list_frontend.point_list))
        self.widget.add_rect_button.pressed.connect(self.point_list_frontend.update_view_point)

    def connect_image(self, image: ImageWidget):
        self.image = image
        self.image.mousePressEvent = self.get_pos


    def get_pos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.widget.draw_tabs.currentWidget() == self.widget.point_tab:
            self.widget.x_point_input.setValue(x)
            self.widget.y_point_input.setValue(y)
            self.draw_point()
        elif self.widget.draw_tabs.currentWidget() == self.widget.line_tab:
            if not self.flag_first_line:
                self.widget.x_start_line_input.setValue(x)
                self.widget.y_start_line_input.setValue(y)
            else:
                self.widget.x_end_line_input.setValue(x)
                self.widget.y_end_line_input.setValue(y)
                self.draw_line()
            self.flag_first_line = not self.flag_first_line
        elif self.widget.draw_tabs.currentWidget() == self.widget.rectangle_tab:
            if not self.flag_first_rect:
                self.widget.x_start_rect_input.setValue(x)
                self.widget.y_start_rect_input.setValue(y)
            else:
                self.widget.x_end_rect_input.setValue(x)
                self.widget.y_end_rect_input.setValue(y)
                self.draw_rectangle()
            self.flag_first_rect = not self.flag_first_rect

    def draw_point(self):
        self.image.draw_point(self.widget.x_point_input.value(), self.widget.y_point_input.value())

    def draw_line(self):
        x1 = self.widget.x_start_line_input.value()
        x2 = self.widget.x_end_line_input.value()
        y1 = self.widget.y_start_line_input.value()
        y2 = self.widget.y_end_line_input.value()
        self.image.draw_line(x1, x2, y1, y2)

    def draw_rectangle(self):
        x1 = self.widget.x_start_rect_input.value()
        x2 = self.widget.x_end_rect_input.value()
        y1 = self.widget.y_start_rect_input.value()
        y2 = self.widget.y_end_rect_input.value()
        self.image.draw_rect(x1, x2, y1, y2)
