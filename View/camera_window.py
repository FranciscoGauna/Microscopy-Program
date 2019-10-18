from lantz.qt import Frontend
from lantz.qt.connect import connect_feat
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage

from Backend.rect_backend import RectangleController
from View.localization import locale
from View.frontend.point_list import PointList
from View.frontend.FrequencyStepFrontend import FrequencyStepFrontend
from View.widgets.custom_image import ImageWidget
from Backend.camera_backend import CameraBackend
from Backend.points_backend import PointController
from Backend.lines_backend import LineController
from Backend.frequency_backend import FrequencyController
import cv2


class CameraControlUi(Frontend):
    backend: CameraBackend
    gui = ('frontend', 'UI', 'camera_button.ui')
    timer = QTimer()
    old_paint_event = None
    flag_first_line = False
    flag_first_rect = False
    point_list_frontend: PointList
    image: ImageWidget
    frequency_frontend: FrequencyStepFrontend
    point_controller: PointController
    line_controller: LineController
    rect_controller: RectangleController

    def setupUi(self):
        self.widget.snap_button.setText(locale.get("start_camera", "str_start_camera"))

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

    def connect_backend(self):
        self.point_list_frontend = PointList(backend=[])

        freq_backend = FrequencyController()
        self.frequency_frontend = FrequencyStepFrontend(backend=freq_backend)
        self.frequency_frontend.widget.oper_order_cb.currentIndexChanged.connect(self.point_list_frontend.update_view_point)
        self.point_controller = PointController(freq_backend)
        self.line_controller = LineController(freq_backend)
        self.rect_controller = RectangleController(freq_backend)
        self.widget.sweep_layout.addWidget(self.frequency_frontend.widget)

        self.widget.sweep_layout.addWidget(self.point_list_frontend.widget)

        self.timer.setInterval(15)
        self.timer.timeout.connect(self.put_photo)
        self.widget.snap_button.pressed.connect(self.start_stop)
        self.image = ImageWidget(self.take_photo())
        self.widget.camera_layout.addWidget(self.image)
        self.image.mousePressEvent = self.get_pos

        connect_feat(self.widget.exposure_time_input, self.backend, "exposure")

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

    def start_stop(self):
        if self.timer.isActive():
            self.widget.snap_button.setText(locale.get("start_camera", "str_start_camera"))
            self.timer.stop()
        else:
            self.widget.snap_button.setText(locale.get("stop_camera", "str_stop_camera"))
            self.timer.start()

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

    def put_photo(self):
        self.image.set_image(self.take_photo())

    def take_photo(self):
        frame = self.backend.snap()
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        reconvert = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
        reconvert = QPixmap.fromImage(reconvert)
        pixmap = QPixmap(reconvert)
        return pixmap
