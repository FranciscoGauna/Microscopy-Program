import cv2
from Drivers.Motor.MotorDriver import Motor, get_available_motors

filename = "name.jpg"

cv2.destroyAllWindows()
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

motor = Motor()
motor.open_motor(get_available_motors()["b'8CMA06-25_15'"], open("8MTF-75LS05.cfg"))
position = motor.position()
print(position[0])
print(position[1])

ret, frame = cap.read()
cv2.imwrite(filename, frame)

cap.release()
cv2.destroyAllWindows()
