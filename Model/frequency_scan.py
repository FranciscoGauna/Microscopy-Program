from Model.AnfatecDriver import AnfatecAMU24
from Model.MotorDriver import Motor
from Model.point import Point
from Backend.platina_backend import PlatinaBackend
from lantz import Q_
from time import sleep
from datetime import datetime

from magic_numbers import pixel_to_counts_factor


def frequency_scanner_linear(inst: AnfatecAMU24, start: int, end: int, step: int):
    """Scans the frequency range given linearly and stores the 4 channel values in the range of the lockin. The lockin
    should be preconfigured with the values you want to use."""
    if end < start:
        raise ValueError("End frequency should be bigger than start frequency")

    time_constant_list = [0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    inst.pll = False
    results = []
    while start < end:
        inst.lockin_frequency = Q_(start, "hertz")
        sleep(time_constant_list[inst.time_constant()] * 0.001 * 10)
        results.append([])
        results[-1].append(start)
        results[-1].append(inst.real_part_x())
        results[-1].append(inst.imaginary_part_y())
        results[-1].append(inst.amplitude)
        results[-1].append(inst.phase)
        start += step

    return results


def frequency_scanner_point(points: list, platina: PlatinaBackend):
    time = datetime.now()
    for point in points:
        x_count = point.x * pixel_to_counts_factor
        y_count = point.y * pixel_to_counts_factor
        platina.move_to(x_count, y_count)
        while not platina.stopped(time):
            sleep(0.01)
        print(datetime.now()-time)


def test():
    platini = PlatinaBackend(Motor(), Motor())
    platini.set_motor_x("virtual")
    cfg_name = "fast_config.cfg"
    cfg = open(cfg_name, "r+")
    platini.set_motor_y(platini.motors[list(platini.motors.keys())[0]], cfg)
    file_name = "test.csv"
    file = open(file_name, "r+")
    points_read = []
    for line in file:
        point_data = line.split(",")
        points_read.append(Point(float(point_data[0]), float(point_data[1]), int(point_data[2]), float(point_data[3])))
    print(points_read)
    frequency_scanner_point(points_read, platini)
