import sys
import random
from typing import List, Dict, Any

import matplotlib

from PyQt5 import QtCore, QtWidgets
from SER.interfaces import ProcessDataUI

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class PlotCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PlotCanvas, self).__init__(fig)

    def update_plot(self, x_data, y_data):
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(x_data, y_data, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()


class LineMapper(ProcessDataUI):
    x_data: List
    y_data: List
    canvas: PlotCanvas

    def __init__(self, x_variable: tuple[str, str, str], y_variable: tuple[str, str, str], max_points=50,
                 x=0, y=0, parent=None, backend=None):
        super().__init__(x, y, parent, backend)
        self.x_device, self.x_var_name, self.x_display_name = x_variable
        self.y_device, self.y_var_name, self.y_display_name = y_variable
        self.max_points = max_points

    def initialize(self):
        self.x_data = []
        self.y_data = []
        self.canvas = PlotCanvas()
        self.setCentralWidget(self.canvas)

    def add_data(self, data: List[Dict[str, Dict[str, Any]]]):
        for datum in data:
            if self.x_device in datum and self.y_device in datum:
                self.x_data.append(datum[self.x_device][self.x_var_name])
                self.y_data.append(datum[self.y_device][self.y_var_name])

        if len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            self.y_data.pop(0)

        self.canvas.update_plot(self.x_data, self.y_data)
