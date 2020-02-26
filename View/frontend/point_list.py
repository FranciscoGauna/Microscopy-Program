import json
import traceback
from typing import List
from logging import ERROR

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant, Qt
from PyQt5.QtWidgets import QFileDialog
from lantz.qt import Frontend

from Model.operation import Operation, PointOperation, LineOperation, RectOperation
from View.localization import locale
from Model.point import Point


class OperationList(Frontend):
    backend: list
    operation_list = []
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
        model = PointTableModel(self.operation_list)
        self.widget.point_list_view.setModel(model)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "Comma Separated Values (*.csv);;All Files (*)", options=options)
        if file_name:
            file = open(file_name, "r+")
            operations_read = []
            data = json.load(file)
            for d in data:
                if d["type"] == "point":
                    operations_read.append(PointOperation(d["x1"], d["y1"], d["start_f"], d["end_f"], d["amount_f"], d["scale"], d["amount_repeat"]))
                if d["type"] == "line":
                    operations_read.append(LineOperation(d["x1"], d["x2"], d["y1"], d["y2"], d["x_amount"], d["start_f"], d["end_f"], d["amount_f"], d["scale"], d["amount_repeat"]))
                if d["type"] == "rect":
                    operations_read.append(RectOperation(d["x1"], d["x2"], d["y1"], d["y2"], d["x_amount"], d["y_amount"], d["start_f"], d["end_f"], d["amount_f"], d["scale"], d["amount_repeat"]))
            self.operation_list = operations_read
            self.update_view_point()

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                   "Comma Separated Values (*.csv);;All Files (*)", options=options)
        if file_name:
            file = open(file_name, "w+")
            file.write(json.dumps(self.operation_list, default=lambda x: x.__dict__))
            file.close()


class PointTableModel(QAbstractTableModel):
    operation_list: List[Operation]

    def __init__(self, operation_list: list):
        super().__init__()
        self.operation_list = operation_list

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 10

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.operation_list)

    def data(self, index: QModelIndex, role: int = ...):
        operation = self.operation_list[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return operation.type_localized()
            if index.column() == 1:
                return operation.total()
            if index.column() == 2:
                return operation.x_range()
            if index.column() == 3:
                return operation.y_range()
            if index.column() == 4:
                return operation.x_amount
            if index.column() == 5:
                return operation.y_amount
            if index.column() == 6:
                return operation.f_range()
            if index.column() == 7:
                return operation.amount_f
            if index.column() == 8:
                return operation.scale
            if index.column() == 9:
                return operation.amount_repeat

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return locale.get("operation", "str_operation")
            if section == 1:
                return locale.get("total_points", "str_total_points")
            if section == 2:
                return locale.get("x_range", "str_x_range")
            if section == 3:
                return locale.get("y_range", "str_y_range")
            if section == 4:
                return locale.get("x_amount", "str_x_amount")
            if section == 5:
                return locale.get("y_amount", "str_y_amount")
            if section == 6:
                return locale.get("frequency_range", "str_frequency_range")
            if section == 7:
                return locale.get("frequency_amount", "str_frequency_amount")
            if section == 8:
                return locale.get("frequency_scale", "str_frequency_scale")
            if section == 9:
                return locale.get("repeat_amount", "str_repeat_amount")

        return QVariant()
