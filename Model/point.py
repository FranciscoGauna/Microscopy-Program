from PyQt5.QtGui import QStandardItem


class Point(QStandardItem):

    def __init__(self, x: int, y: int, freq: int, n=1):
        super().__init__()
        self.x = x
        self.y = y
        self.frequency = freq
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

    def __lt__(self, other):
        if self.frequency.__lt__(other.frequency):
            return self.frequency.__lt__(other.frequency)
        if self.x.__lt__(other.x):
            return self.x.__lt__(other.x)
        if self.y.__lt__(other.y):
            return self.y.__lt__(other.y)
        return False

    def __le__(self, other):
        if self == other: return True
        if self.frequency.__lt__(other.frequency):
            return self.frequency.__lt__(other.frequency)
        if self.x.__lt__(other.x):
            return self.x.__lt__(other.x)
        if self.y.__lt__(other.y):
            return self.y.__lt__(other.y)
        return False

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other


    def __str__(self):
        return "x:" + str(self.x) + ",y:" + str(self.y) + ",frequency:" + str(self.frequency) + ",ammount:" + str(
            self.n)


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
