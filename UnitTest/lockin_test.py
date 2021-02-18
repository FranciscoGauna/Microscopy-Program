from Drivers.Lockin.LI5655 import LI5655


def test():
    driver = LI5655("dummmy")
    driver.initialize()

    print(driver.real_part_x)
    print(driver.imaginary_part_y)
    print(driver.amplitude)
    print(driver.phase)

    print(driver.frequency)

    print(driver.harmonic)
    driver.harmonic = 2
    print(driver.harmonic)

    print(driver.overloaded)

    print(driver.reference_internal)
    driver.reference_internal = True
    print(driver.reference_internal)



if __name__ == "__main__":
    test()
