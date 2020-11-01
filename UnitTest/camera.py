import cv2
from random import shuffle
from Drivers.Motor.MotorDriver import get_available_motors, Motor
from time import sleep
from os.path import exists


def test():
    cv2.destroyAllWindows()
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)

    motor = Motor()
    motor.open_motor(get_available_motors()["b'8CMA06-25_15'"], open("8MTF-75LS05.cfg"))

    puntos = [300000, 296000, 292000, 288000, 284000, 300000, 296000, 292000, 288000, 284000, 280000, 280000]
    shuffle(puntos)

    for punto in puntos:
        result = motor.move_to(punto)
        if not result:
            print("fail motor")
        while not motor.stopped():
            sleep(0.1)
        ret, frame = cap.read()
        if not ret:
            print("Fail")
        else:
            filename = str(punto) + '_0.png'
            filedata = str(punto) + '_0.txt'
            if exists(filename):
                filename = str(punto) + '_1.png'
                filedata = str(punto) + '_1.txt'
            position = motor.position()
            print("Punto: " + str(punto) + " , Posicion: " + str(position[0]))
            with open(filedata, "w+") as file:
                file.write(str(position[0]) + "," + str(position[1]))

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main":
    test()
