import os

from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QFileDialog
from lantz.qt import Frontend

from View.localization import locale
from Model.point import Point


class PointList(Frontend):
    backend: list
    point_list = []
    gui = ("UI", "point_list.ui")

    def setupUi(self):
        super().setupUi()
        self.widget.save_button.setText(locale.get("save", "str_save"))
        self.widget.load_button.setText(locale.get("load", "str_load"))

    def connect_backend(self):
        super().connect_backend()
        self.widget.save_button.pressed.connect(self.save_file)
        self.widget.load_button.pressed.connect(self.open_file)

    def update_view_point(self):
        self.point_list = sorted(self.point_list)
        string_list = []
        for point in self.point_list:
            string_list.append(str(point))
        model = QStringListModel(string_list)
        self.widget.point_list_view.setModel(model)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "Comma Separated Values (*.csv);;All Files (*)", options=options)
        if file_name:
            file = open(file_name, "r+")
            points_read = []
            for line in file:
                point_data = line.split(",")
                try:
                    points_read.append(Point(float(point_data[0]), float(point_data[1]), int(point_data[2]), float(point_data[3])))
                except Exception:
                    pass
            self.point_list = points_read
            self.update_view_point()

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                   "Comma Separated Values (*.csv);;All Files (*)", options=options)
        if file_name:
            file = open(file_name, "w+")
            for point in self.point_list:
                file.write(str(point.x))
                file.write(",")
                file.write(str(point.y))
                file.write(",")
                file.write(str(point.frequency))
                file.write(",")
                file.write(str(point.n))
                if point is not self.point_list[-1]:
                    file.write("\n")
