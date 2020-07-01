import datetime


class ResultPoint:
    x: float
    y: float
    display_x: int
    display_y: int
    freq: float
    value: float
    amplitude: float
    phase: float
    real_part: float
    imag_part: float
    repeat_n: int
    type: int
    time: datetime.timedelta

    def __init__(self, x_count, y_count, frequency, amp, phase, real_part, imag_part, display_x, display_y, time):
        self.x = x_count
        self.y = y_count
        self.freq = frequency
        self.value = amp
        self.amplitude = amp
        self.phase = phase
        self.imag_part = imag_part
        self.real_part = real_part
        self.display_x = display_x
        self.display_y = display_y
        self.time = time

    def to_file(self):
        string = ""
        string += str(self.x) + "\t"
        string += str(self.y) + "\t"
        string += str(self.display_x) + "\t"
        string += str(self.display_y) + "\t"
        string += str(self.freq) + "\t"
        string += str(self.value) + "\t"
        string += str(self.time.total_seconds())
        return string
