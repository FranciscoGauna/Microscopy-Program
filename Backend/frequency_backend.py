from lantz.qt import Backend
from lantz.core import Feat
from Model.scaler import ScalerController
from Model.point import Point, change_ordering
from View.localization import locale


class FrequencyController(Backend):
    _start_f = 1
    _end_f = 1
    _amount_f = 1
    _amount_repeat = 1
    scaler = ScalerController()

    def make_points(self, x, y):
        return self.scaler.make_points(x, y, self._start_f, self._end_f, self._amount_f, self._amount_repeat)

    @Feat()
    def start_f(self):
        return self._start_f

    @start_f.setter
    def start_f(self, start_f):
        self._start_f = start_f

    @Feat()
    def end_f(self):
        return self._end_f

    @end_f.setter
    def end_f(self, end_f):
        self._end_f = end_f

    @Feat()
    def amount_f(self):
        return self._amount_f

    @amount_f.setter
    def amount_f(self, amount_f):
        self._amount_f = amount_f

    @Feat()
    def amount_repeat(self):
        return self._amount_repeat

    @amount_repeat.setter
    def amount_repeat(self, amount_repeat):
        self._amount_repeat = amount_repeat

    @Feat(values={
        locale.get("linear", "str_linear"): "linear",
        locale.get("log", "str_log"): "log"})
    def scale(self):
        return self.scaler.scale()

    @scale.setter
    def scale(self, scale):
        self.scaler.set_scale(scale)

    @Feat(values={
        locale.get("pos_order", "str_pos_order"): "pos",
        locale.get("freq_order", "str_freq_order"): "freq"})
    def point_order(self):
        return Point._ordering

    @point_order.setter
    def point_order(self, order):
        change_ordering(order)
