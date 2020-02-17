from lantz.qt import Backend
from lantz.core import Feat
from Backend.frequency_backend import FrequencyController
from Model.operation import PointOperation


class PointController(Backend):
    _x = 0
    _y = 0
    freq_backend: FrequencyController

    def __init__(self, freq_backend: FrequencyController, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.freq_backend = freq_backend

    def add_point(self, point_list):
        point_operation = PointOperation(self._x, self._y, self.freq_backend.start_f, self.freq_backend.end_f,
                                         self.freq_backend.amount_f, self.freq_backend.int_scale(),
                                         self.freq_backend.amount_repeat)
        point_list.append(point_operation)

    @Feat()
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @Feat()
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
