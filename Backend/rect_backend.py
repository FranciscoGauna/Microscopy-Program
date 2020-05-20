from lantz.qt import Backend
from lantz.core import Feat

from Model.operation import RectOperation
from Model.scaler import lin_list
from Backend.frequency_backend import FrequencyController


class RectangleController(Backend):
    _x_start = 0
    _x_end = 0
    _y_start = 0
    _y_end = 0
    _x_steps = 2
    _y_steps = 2
    freq_backend: FrequencyController

    def __init__(self, freq_backend: FrequencyController, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.freq_backend = freq_backend

    def add_rect(self, point_list):
        operation = RectOperation(self._x_start, self._x_end, self._y_start, self._y_end, self._x_steps, self._y_steps,
                                  self.freq_backend.start_f, self.freq_backend.end_f, self.freq_backend.amount_f,
                                  self.freq_backend.int_scale(), self.freq_backend.amount_repeat,
                                  self.freq_backend.point_order_backend())
        point_list.append(operation)

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
    def x_steps(self):
        return self._x_steps

    @x_steps.setter
    def x_steps(self, x_steps):
        self._x_steps = x_steps

    @Feat()
    def y_steps(self):
        return self._y_steps

    @y_steps.setter
    def y_steps(self, y_steps):
        self._y_steps = y_steps
