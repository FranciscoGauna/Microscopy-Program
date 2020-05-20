from Model.point import Point
from math import sqrt


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


def lin_list(start, end, n: int):
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


def make_freq_in_points(x, y, f_s, f_e, n, m, scale, display_x):
    results = []
    display_y = 0
    list_freq = freq_list_scale(f_s, f_e, n, scale)
    for freq in list_freq:
        results.append(Point(x, y, freq, m, display_x, display_y))
        display_y += 1
    return results


def freq_list_scale(f_s, f_e, n, scale):
    if scale == "linear":
        list_freq = lin_list(f_s, f_e, n)
    else:
        list_freq = log_list(f_s, f_e, n)
    return list_freq


def square_list(start: int, end: int, n: int) -> list:
    if start > end:
        temp = start
        start = end
        end = temp
    if n < 1:
        raise ValueError("n < 1")
    if n == 1:
        return [start]
    results = []
    c = (pow(end, 2) - pow(start, 2)) / (n - 1)
    results.append(start)
    for i in range(1, n):
        results.append(sqrt(pow(results[i-1], 2) + c))
    return results
