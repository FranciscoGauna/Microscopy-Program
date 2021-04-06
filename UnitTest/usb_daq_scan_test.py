def test():
    from ctypes.wintypes import WORD
    from time import sleep

    from mcculw.ul import a_in_scan, win_buf_alloc, win_buf_to_array, win_buf_free
    from mcculw.enums import ULRange

    # Duracion en segundos
    duration = 10
    # Primer Canal
    low_channels = 0
    # Ultimo Canal
    high_channels = 3
    # Cantidad de muestras por segundo
    rate = 1000

    # ----------------------------------- Code Starts Here ----------------------------------------------------------- #

    number_points = rate * duration * (high_channels - low_channels + 1)
    array_pointer = win_buf_alloc(number_points)
    if array_pointer == 0:
        raise Exception("Failed Memory Allocation")
    if rate != a_in_scan(1, low_channels, high_channels, number_points, rate, ULRange.BIP5VOLTS, array_pointer, 0):
        raise Exception("Rate Too High")

    ArrayType = WORD * number_points

    c_array = ArrayType()
    win_buf_to_array(array_pointer, c_array, 0, number_points)

    c_array_2 = ArrayType()
    win_buf_to_array(array_pointer, c_array_2, 0, number_points)

    output_file = open("output.log", "w+")
    index = 0
    for data_point in c_array:
        output_file.write(str(data_point))
        if index < 3:
            output_file.write(',')
            index += 1
        else:
            output_file.write('\n')
            index = 0
    output_file.close()
    output_file = open("output2.log", "w+")
    index = 0
    for data_point in c_array_2:
        output_file.write(str(data_point))
        if index < 3:
            output_file.write(',')
            index += 1
        else:
            output_file.write('\n')
            index = 0
    output_file.close()

    win_buf_free(array_pointer)


if __name__ == "__main__":
    test()
