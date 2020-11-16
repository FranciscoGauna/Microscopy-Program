from lantz.qt import Backend
from lantz.core import Feat
from View.localization import locale


class FrequencyController(Backend):
    """
    This class administers the logic for the Frequency controller widget and is an useful interface for the frontend
    to connect the feats to widgets.
    """
    _start_f = 1
    _end_f = 1
    _amount_f = 1
    _amount_repeat = 1
    _scale = "log"
    _order = "pos"

    @Feat()
    def start_f(self):
        """Getter for the first frequency to read"""
        return self._start_f

    @start_f.setter
    def start_f(self, start_f):
        """Setter for the first frequency to read"""
        self._start_f = start_f

    @Feat()
    def end_f(self):
        """Getter for the last frequency to read"""
        return self._end_f

    @end_f.setter
    def end_f(self, end_f):
        """Setter for the last frequency to read"""
        self._end_f = end_f

    @Feat()
    def amount_f(self):
        """Getter for the amount of different frequencies to dread"""
        return self._amount_f

    @amount_f.setter
    def amount_f(self, amount_f):
        """Setter for the amount of different frequencies to dread"""
        self._amount_f = amount_f

    @Feat()
    def amount_repeat(self):
        """Getter for the amount of times the same frequency repeats to get an average sample"""
        return self._amount_repeat

    @amount_repeat.setter
    def amount_repeat(self, amount_repeat):
        """Setter for the amount of times the same frequency repeats to get an average sample"""
        self._amount_repeat = amount_repeat

    @Feat(values={
        locale.get("linear", "str_linear"): "linear",
        locale.get("log", "str_log"): "log"})
    def scale(self):
        """
        Getter for the way the frequencies should be distributed
        :return: either "linear" for a linear distribution, or "log" for a logarithmic distribution
        """
        return self._scale

    @scale.setter
    def scale(self, scale):
        """
        Setter for the way the frequencies should be distributed
        :param scale:  either "linear" for a linear distribution, or "log" for a logarithmic distribution
        :return: none
        """
        self._scale = scale

    def int_scale(self):
        """ Getter for the scale without using a property wrapper. """
        return self._scale

    @Feat(values={
        locale.get("pos_order", "str_pos_order"): "pos",
        locale.get("freq_order", "str_freq_order"): "freq"})
    def point_order(self):
        """
        Getter for the point order. :return: either "pos" for operations that are ordered by position first or "freq"
        for operations that are ordered by frequncy first."""
        return self._order

    @point_order.setter
    def point_order(self, order):
        """
        Setter for the point order.
        :param order: either "pos" for operations that are ordered by position first or "freq"
        for operations that are ordered by frequncy first.
        :return: None
        """
        self._order = order

    def point_order_backend(self):
        """Getter for the point order. :return: either "pos" for operations that are ordered by position first or "freq"
        for operations that are ordered by frequncy first. Useful when you need to use a function and not a wrapper"""
        return self._order
