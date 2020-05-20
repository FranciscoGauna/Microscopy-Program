from abc import abstractmethod, ABC
from typing import List

from Model.point import Point
from Model.scaler import make_freq_in_points, lin_list, freq_list_scale
from View.localization import locale


class Operation(ABC):
    x1: float
    x2: float
    y1: float
    y2: float
    x_amount: int
    y_amount: int
    start_f: float
    end_f: float
    amount_f: int
    amount_repeat: int
    order: str
    scale: str
    type: str

    @abstractmethod
    def to_points(self) -> List[Point]:
        pass

    @abstractmethod
    def total(self) -> int:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def x_range(self) -> str:
        pass

    @abstractmethod
    def y_range(self) -> str:
        pass

    def f_range(self) -> str:
        return str(self.start_f) + "-" + str(self.end_f)

    def update_offset(self, x_o, y_o):
        self.x1 += x_o
        self.x2 += x_o
        self.y1 += y_o
        self.y2 += y_o

    def type_localized(self):
        return locale.get(self.type, "str_" + self.type)


class PointOperation(Operation):

    def __init__(self, x, y, start_f, end_f, amount_f, scale, repeat):
        self.x1 = self.x2 = x
        self.y1 = self.y2 = y
        self.x_amount = self.y_amount = 1
        self.start_f = start_f
        self.end_f = end_f
        self.amount_f = amount_f
        self.scale = scale
        self.amount_repeat = repeat
        self.type = "point"
        self.order = "freq"

    def total(self) -> int:
        return self.amount_f

    def height(self) -> int:
        return self.amount_f

    def width(self) -> int:
        return 1

    def x_range(self) -> str:
        return str(self.x1)

    def y_range(self) -> str:
        return str(self.y1)

    def to_points(self) -> List[Point]:
        return make_freq_in_points(self.x1, self.y1, self.start_f, self.end_f, self.amount_f, self.amount_repeat,
                                   self.scale, 0)


class LineOperation(Operation):

    def __init__(self, x_1, x_2, y_1, y_2, line_amount, start_f, end_f, amount_f, scale, repeat, order):
        self.x1 = x_1
        self.x2 = x_2
        self.y1 = y_1
        self.y2 = y_2
        self.x_amount = self.y_amount = line_amount
        self.start_f = start_f
        self.end_f = end_f
        self.amount_f = amount_f
        self.scale = scale
        self.amount_repeat = repeat
        self.type = "line"
        self.order = order

    def x_range(self) -> str:
        return str(self.x1) + "-" + str(self.x2)

    def y_range(self) -> str:
        return str(self.y1) + "-" + str(self.y2)

    def total(self) -> int:
        return self.x_amount * self.amount_f

    def height(self) -> int:
        if self.order == "freq":
            return self.amount_f
        return self.x_amount

    def width(self) -> int:
        if self.order == "pos":
            return self.amount_f
        return self.x_amount

    def to_points(self):
        results = []
        x_range = lin_list(int(self.x1), int(self.x2), self.x_amount)
        y_range = lin_list(int(self.y1), int(self.y2), self.y_amount)
        if self.order == "freq":
            for i in range(self.x_amount):
                results.extend(make_freq_in_points(x_range[i], y_range[i], self.start_f, self.end_f, self.amount_f,
                                                   self.amount_repeat, self.scale, i))
        else:
            list_freq = freq_list_scale(self.start_f, self.end_f, self.amount_f, self.scale)
            for f_index in range(self.amount_f):
                for x_index in range(0, self.x_amount):
                    results.append(Point(x_range[x_index], y_range[x_index], list_freq[f_index], self.amount_repeat,
                                         f_index, x_index))
        return results


class RectOperation(Operation):

    def __init__(self, x_1, x_2, y_1, y_2, x_amount, y_amount, start_f, end_f, amount_f, scale, repeat, order):
        self.x1 = x_1
        self.x2 = x_2
        self.y1 = y_1
        self.y2 = y_2
        self.x_amount = x_amount
        self.y_amount = y_amount
        self.start_f = start_f
        self.end_f = end_f
        self.amount_f = amount_f
        self.scale = scale
        self.amount_repeat = repeat
        self.type = "rect"
        self.order = order

    def x_range(self) -> str:
        return str(self.x1) + "-" + str(self.x2)

    def y_range(self) -> str:
        return str(self.y1) + "-" + str(self.y2)

    def total(self) -> int:
        return self.x_amount * self.y_amount * self.amount_f

    def height(self) -> int:
        if self.order == "freq":
            return self.amount_f
        return self.y_amount

    def width(self) -> int:
        if self.order == "pos":
            return self.x_amount
        return self.y_amount

    def to_points(self):
        results = []
        x_range = lin_list(int(self.x1), int(self.x2), self.x_amount)
        y_range = lin_list(int(self.y1), int(self.y2), self.y_amount)
        if self.order == "freq":
            for j in range(0, self.y_amount):
                for i in range(0, self.x_amount):
                    results.extend(make_freq_in_points(x_range[i], y_range[j], self.start_f,  self.end_f,
                                                       self.amount_f, self.amount_repeat, self.scale, i))
        else:
            list_freq = freq_list_scale(self.start_f, self.end_f, self.amount_f, self.scale)
            for f in list_freq:
                for y in range(0, self.y_amount):
                    for x in range(0, self.x_amount):
                        results.append(Point(x_range[x], y_range[x], f, self.amount_repeat, y, x))
            print(results)
        return results
