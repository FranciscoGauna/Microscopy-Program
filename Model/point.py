from math import trunc


def change_ordering(set_ordering):
    if set_ordering == "freq":
        Point._ordering = set_ordering
        Point.__lt__ = Point._freq_order
    if set_ordering == "pos":
        Point._ordering = set_ordering
        Point.__lt__ = Point._position_order


class Point:
    _ordering = "freq"

    def __init__(self, x: float, y: float, freq: int, n=1, display_x: int = 0, display_y: int = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.frequency = freq
        self.display_x = display_x
        self.display_y = display_y
        if n < 1:
            raise ValueError
        self.n = n

    def __eq__(self, other):
        if not other.frequency.__eq__(self.frequency):
            return other.frequency.__eq__(self.frequency)
        if not other.x.__eq__(self.x):
            return other.x.__eq__(self.x)
        if not other.y.__eq__(self.y):
            return other.y.__eq__(self.y)
        return True

    def _freq_order(self, other):
        if self.frequency != other.frequency:
            return self.frequency < other.frequency
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        return False

    def _position_order(self, other):
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        if self.frequency != other.frequency:
            return self.frequency < other.frequency
        return False

    def __lt__(self, other):
        if self.frequency != other.frequency:
            return self.frequency < other.frequency
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        return False

    def __le__(self, other):
        if self == other or self < other: return True
        return False

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __str__(self):
        return "x: " + str(trunc(self.x)) + "\ty: " + str(trunc(self.y)) + "\tfrequency: " + str(trunc(self.frequency)) +\
        "\t\trepeat: " + str(self.n)


if __name__ == "__main__":
    print("Test equal points")
    assert (Point(0, 0, 0) == Point(0, 0, 0))
    print("Test equality different points")
    assert (Point(0, 0, 0) != Point(1, 0, 0))
    assert (Point(0, 0, 0) != Point(0, 1, 0))
    assert (Point(0, 0, 0) != Point(0, 0, 1))

    print("Compare lt same points")
    assert (not Point(0, 0, 0) < Point(0, 0, 0))
    print("Compare lt different points")
    assert (Point(0, 0, 0) < Point(1, 0, 0))
    assert (Point(0, 0, 0) < Point(0, 1, 0))
    assert (Point(0, 0, 0) < Point(0, 0, 1))

    print("Compare le same points")
    assert (Point(0, 0, 0) <= Point(0, 0, 0))
    print("Compare le different points")
    assert (Point(0, 0, 0) <= Point(1, 0, 0))
    assert (Point(0, 0, 0) <= Point(0, 1, 0))
    assert (Point(0, 0, 0) <= Point(0, 0, 1))

    print("Compare gt same points")
    assert (not Point(0, 0, 0) > Point(0, 0, 0))
    print("Compare gt different points")
    assert (not Point(0, 0, 0) > Point(1, 0, 0))
    assert (Point(1, 0, 0) > Point(0, 0, 0))
    assert (not Point(0, 0, 0) > Point(0, 1, 0))
    assert (Point(0, 1, 0) > Point(0, 0, 0))
    assert (not Point(0, 0, 0) > Point(0, 0, 1))
    assert (Point(0, 0, 1) > Point(0, 0, 0))

    print("Compare gt same points")
    assert (Point(0, 0, 0) >= Point(0, 0, 0))
    print("Compare gt different points")
    assert (not Point(0, 0, 0) >= Point(1, 0, 0))
    assert (Point(1, 0, 0) >= Point(0, 0, 0))
    assert (not Point(0, 0, 0) >= Point(0, 1, 0))
    assert (Point(0, 1, 0) >= Point(0, 0, 0))
    assert (not Point(0, 0, 0) >= Point(0, 0, 1))
    assert (Point(0, 0, 1) >= Point(0, 0, 0))

    print("Compare complex points")
    top_left = Point(0, 0, 0)
    bot_left = Point(0, 1, 0)
    bot_right = Point(1, 1, 0)
    top_right = Point(1, 0, 0)
    assert (top_left < bot_left)
    assert (top_left < bot_right)
    assert (top_left < top_right)
    assert bot_left < top_right

    print("Ordered List")
    top_right = Point(251, 56, 7)
    top_left = Point(105, 57, 7)
    bot_left = Point(105, 247, 7)
    bot_right = Point(296, 180, 7)
    lista = [top_right, top_left, bot_right, bot_left]
    srt_lista = sorted(lista)
    for i in range(0, len(lista)):
        print("Lista:  "+str(lista[i]))
        print("Sorted: "+str(srt_lista[i]))

    print("Barrido en frecuencia vs Barrido en posicion")
    top_right_7 = Point(251, 56, 7)
    top_right_10 = Point(251, 56, 10)
    top_right_20 = Point(251, 56, 20)
    top_left_7 = Point(105, 57, 7)
    top_left_10 = Point(105, 57, 10)
    top_left_20 = Point(105, 57, 20)
    lista = [top_right_7, top_right_10, top_left_7, top_left_10, top_left_20, top_right_20]
    lista_string = ""
    srt_lista = sorted(lista)
    lista_string_string = ""
    change_ordering("pos")
    pos_lista = sorted(lista)
    pos_lista_string = ""
    for i in range(0, len(lista)):
        lista_string += str(lista[i]) + "\t\t"
        lista_string_string += str(srt_lista[i]) + "\t\t"
        pos_lista_string += str(pos_lista[i]) + "\t\t"
    print("Lista:\t\t\t" + lista_string)
    print("Sorted Freq:\t" + lista_string_string)
    print("Sorted Pos:\t\t" + pos_lista_string)
