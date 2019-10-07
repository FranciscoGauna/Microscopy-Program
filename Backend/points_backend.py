from lantz.qt import Backend
from lantz.core import Feat
from Backend.frequency_backend import FrequencyController


class PointController(Backend):
    _x = 0
    _y = 0
    freq_backend: FrequencyController

    def __init__(self, freq_backend: FrequencyController, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.freq_backend = freq_backend

    def add_point(self, point_list):
        point_list.extend(self.freq_backend.make_points(self._x, self._y))
        for element in point_list:
            print(element)

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
