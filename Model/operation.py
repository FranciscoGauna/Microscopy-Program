from abc import abstractmethod, ABC
from typing import List

from Model.point import Point
from Model.scaler import ScalerController, lin_list
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
    point_order: str
    scaler = ScalerController()
    type: str

    @abstractmethod
    def to_points(self) -> list:
        pass

    @abstractmethod
    def total(self) -> int:
        pass

    @abstractmethod
    def x_range(self) -> str:
        pass

    @abstractmethod
    def y_range(self) -> str:
        pass

    def f_range(self) -> str:
        return str(self.start_f) + "-" + str(self.end_f)

    def scale(self) -> str:
        return self.scaler.scale()

    def update_offset(self, x_o, y_o):
        self.x1 += x_o
        self.x2 += x_o
        self.y1 += y_o
        self.y2 += y_o




class PointOperation(Operation):

    type = locale.get("point", "str_point")

    def __init__(self, x, y, start_f, end_f, amount_f, scale, repeat):
        self.x1 = self.x2 = x
        self.y1 = self.y2 = y
        self.x_amount = self.y_amount = 1
        self.start_f = start_f
        self.end_f = end_f
        self.amount_f = amount_f
        self.scaler.set_scale(scale)
        self.amount_repeat = repeat

    def total(self) -> int:
        return self.amount_f

    def x_range(self) -> str:
        return str(self.x1)

    def y_range(self) -> str:
        return str(self.y1)

    def to_points(self) -> List[Point]:
        return self.scaler.make_points(self.x1, self.y1, self.start_f, self.end_f, self.amount_f, self.amount_repeat)


class LineOperation(Operation):

    type = locale.get("line", "str_line")

    def __init__(self, x_1, x_2, y_1, y_2, line_amount, start_f, end_f, amount_f, scale, repeat):
        self.x1 = x_1
        self.x2 = x_2
        self.y1 = y_1
        self.y2 = y_2
        self.x_amount = self.y_amount = line_amount
        self.start_f = start_f
        self.end_f = end_f
        self.amount_f = amount_f
        self.scaler.set_scale(scale)
        self.amount_repeat = repeat

    def x_range(self) -> str:
        return str(self.x1) + "-" + str(self.x2)

    def y_range(self) -> str:
        return str(self.y1) + "-" + str(self.y2)

    def total(self) -> int:
        return self.x_amount * self.amount_f

    def to_points(self):
        results = []
        x_range = lin_list(int(self.x1), int(self.x2), self.x_amount)
        y_range = lin_list(int(self.y1), int(self.y2), self.y_amount)
        for i in range(0, self.x_amount):
            results.extend(self.scaler.make_points(x_range[i], y_range[i], self.start_f, self.end_f, self.amount_f,
                                                   self.amount_repeat))
        return results


class RectOperation(Operation):
    type = locale.get("rect", "str_rect")

    def __init__(self, x_1, x_2, y_1, y_2, x_amount, y_amount, start_f, end_f, amount_f, scale, repeat):
        self.x1 = x_1
        self.x2 = x_2
        self.y1 = y_1
        self.y2 = y_2
        self.x_amount = x_amount
        self.y_amount = y_amount
        self.start_f = start_f
        self.end_f = end_f
        self.amount_f = amount_f
        self.scaler.set_scale(scale)
        self.amount_repeat = repeat

    def x_range(self) -> str:
        return str(self.x1) + "-" + str(self.x2)

    def y_range(self) -> str:
        return str(self.y1) + "-" + str(self.y2)

    def total(self) -> int:
        return self.x_amount * self.y_amount * self.amount_f

    def to_points(self):
        results = []
        x_range = lin_list(int(self.x1), int(self.x2), self.x_amount)
        y_range = lin_list(int(self.y1), int(self.y2), self.y_amount)
        for j in range(0, self.y_amount):
            for i in range(0, self.x_amount):
                results.extend(self.scaler.make_points(x_range[i], y_range[j], self.start_f,
                                                       self.end_f, self.amount_f, self.amount_repeat))
        return results
