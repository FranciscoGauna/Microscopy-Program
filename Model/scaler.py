from Model.point import Point

def log_list(start: int, end: int, n: int) -> list:
    if start > end:
        temp = start
        start = end
        end = temp
    if n < 1 or start <= 0:
        raise ValueError
    if n == 1:
        return [start]
    results = []
    for i in range(0, n):
        results.append(start*pow(end/start, i/(n-1)))
    return results


def lin_list(start: int, end: int, n: int):
    if start > end:
        temp = start
        start = end
        end = temp
    if n < 1:
        raise ValueError
    if n == 1:
        return [start]
    results = []
    step = (end - start) / (n - 1)
    for i in range(0, n):
        results.append(start + i * step)
    return results


def make_points(x, y, f_s, f_e, n, m, scale):
    results = []
    if scale == "linear":
        freqs = lin_list(f_s, f_e, n)
    else:  # elif self._scale == "log"
        freqs = log_list(f_s, f_e, n)
    for freq in freqs:
        results.append(Point(x, y, freq, m))
    return results
