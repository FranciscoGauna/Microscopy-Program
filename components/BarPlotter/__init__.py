import math
from typing import List, Dict, Any

import matplotlib
import numpy as np
from pyqtgraph import PlotWidget, BarGraphItem, PlotItem

from SER.interfaces import ProcessDataUI


class BarPlotter(ProcessDataUI):
    x_data: List
    y_data: List
    canvas: PlotWidget

    def __init__(self, x_variable: tuple[str, str, str], y_variable: tuple[str, str, str], max_points=50, histogram=False,
                 x=0, y=0, parent=None, backend=None):
        """

        Args:
            x_variable:
            y_variable: Note, this is ignored if Histogram is set to true
            max_points:
            Histogram:
            x:
            y:
            parent:
            backend:
        """
        super().__init__(x, y, parent, backend)
        self.x_device, self.x_var_name, self.x_display_name = x_variable
        self.y_device, self.y_var_name, self.y_display_name = y_variable
        # TODO: include display name
        self.max_points = max_points
        self.histogram = histogram
        self.initialize()

    def initialize(self):
        self.x_data = []
        self.y_data = []
        # Here is the plot widget from pyqtgraph
        self.canvas = PlotWidget()
        self.setCentralWidget(self.canvas)

    def add_data(self, data: List[Dict[str, Dict[str, Any]]]):
        item: PlotItem = self.canvas.getPlotItem()
        item.clear()
        for datum in data:
            if self.x_device in datum and self.y_device in datum:
                self.x_data.append(datum[self.x_device][self.x_var_name])
                self.y_data.append(datum[self.y_device][self.y_var_name])

        while len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            self.y_data.pop(0)

        if self.histogram:
            min_val = min(self.y_data)
            max_val = max(self.y_data)
            bucket_count = math.ceil(math.sqrt(len(self.y_data))) + 10
            delta = (max_val - min_val) / bucket_count
            x_data = [min_val + (i * delta) for i in range(bucket_count)]
            y_data = [0 for _ in range(bucket_count)]
            if delta > 0:
                for val in self.y_data:
                    if val == max_val:
                        y_data[-1] += 1
                    else:
                        index = math.floor((val - min_val) / delta)
                        y_data[index] += 1
            else:
                y_data[0] = 1
            # min_val = math.floor(min(self.y_data))
            # max_val = math.ceil(max(self.y_data))
            # x_data = [i for i in range(min_val, max_val + 1)]
            # y_data = [0 for _ in range(min_val, max_val + 1)]
            # for val in self.y_data:
            #     index = math.floor(val) - min_val
            #     y_data[index] += 1
            item.addItem(BarGraphItem(x=x_data, height=y_data, width=1.5, brush='g'))
        else:
            item.addItem(BarGraphItem(x=self.x_data, height=self.y_data, width=1.5, brush='g'))
