from typing import List, Dict, Any

import matplotlib
import numpy as np
from pyqtgraph import PlotWidget

from SER.interfaces import ProcessDataUI


class LinePlotter(ProcessDataUI):
    x_data: List
    y_data: List
    canvas: PlotWidget

    def __init__(self, x_variable: tuple[str, str, str], y_variable: tuple[str, str, str], max_points=50, scatter=False,
                 x=0, y=0, parent=None, backend=None):
        super().__init__(x, y, parent, backend)
        self.x_device, self.x_var_name, self.x_display_name = x_variable
        self.y_device, self.y_var_name, self.y_display_name = y_variable
        self.max_points = max_points
        self.scatter = scatter
        self.initialize()

    def initialize(self):
        self.x_data = []
        self.y_data = []
        # Here is the plot widget from pyqtgraph
        self.canvas = PlotWidget()
        self.setCentralWidget(self.canvas)

    def add_data(self, data: List[Dict[str, Dict[str, Any]]]):
        item = self.canvas.getPlotItem()
        item.clear()
        for datum in data:
            if self.x_device in datum and self.y_device in datum:
                self.x_data.append(datum[self.x_device][self.x_var_name])
                self.y_data.append(datum[self.y_device][self.y_var_name])

        while len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            self.y_data.pop(0)

        if self.scatter:
            connect_data = np.array([0 for i in range(len(self.x_data))])
            item.plot(self.x_data, self.y_data, connect=connect_data, symbol='o', symbolSize=7)
        else:
            item.plot(self.x_data, self.y_data)
