from math import trunc


class Point:
    """Class that represents a point to be measured in the round"""

    def __init__(self, x: float, y: float, freq: int, n=1, display_x: int = 0, display_y: int = 0):
        """

        :param x: X coordinate in the camera that represented this point
        :param y: Y coordinate in the camera that represented this point
        :param freq: Frequeency at wich the point should be measured
        :param n: Amount of times the point should be re read to average the results
        :param display_x: X coordinate where the point should be represented in a map of the operation
        :param display_y: Y coordinate where the point should be represented in a map of the operation
        """
        super().__init__()
        self.x = x
        self.y = y
        self.frequency = freq
        self.display_x = display_x
        self.display_y = display_y
        if n < 1:
            raise ValueError
        self.n = n

    def __str__(self):
        return "x: " + str(trunc(self.x)) + "\ty: " + str(trunc(self.y)) + "\tfrequency: " + str(trunc(self.frequency))\
               + "\t\trepeat: " + str(self.n)
