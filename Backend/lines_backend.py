from lantz.qt import Backend
from lantz.core import Feat
from Model.scaler import lin_list
from Backend.frequency_backend import FrequencyController


class LineController(Backend):
    _x_start = 0
    _x_end = 0
    _y_start = 0
    _y_end = 0
    _line_steps = 2
    freq_backend: FrequencyController

    def __init__(self, freq_backend: FrequencyController, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.freq_backend = freq_backend

    def add_line(self, point_list):
        results = []
        x_range = lin_list(self._x_start, self._x_end, self._line_steps)
        y_range = lin_list(self._y_start, self._y_end, self._line_steps)
        for i in range(0, self._line_steps):
            results.extend(self.freq_backend.make_points(x_range[i], y_range[i]))
        point_list.extend(results)

    @Feat()
    def x_start(self):
        return self._x_start

    @x_start.setter
    def x_start(self, x):
        self._x_start = x

    @Feat()
    def x_end(self):
        return self._x_end

    @x_end.setter
    def x_end(self, x):
        self._x_end = x

    @Feat()
    def y_start(self):
        return self._y_start

    @y_start.setter
    def y_start(self, y):
        self._y_start = y

    @Feat()
    def y_end(self):
        return self._y_end

    @y_end.setter
    def y_end(self, y):
        self._y_end = y

    @Feat()
    def line_steps(self):
        return self._line_steps

    @line_steps.setter
    def line_steps(self, line_steps):
        self._line_steps = line_steps
