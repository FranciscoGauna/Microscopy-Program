import cv2
from sys import getsizeof
from PIL import Image
from datetime import datetime

camera = cv2.VideoCapture(0)
time_0 = datetime.now()
raw_data = camera.read()[1]
try:
    time_1 = datetime.now()
    image = Image.fromarray(raw_data)
    time_2 = datetime.now()
    with open("test.png", "wb+") as file:
        image.save(file, "png")
    time_3 = datetime.now()
    print(f"Read Camera Rime: {time_1 - time_0}\tCreate Image Time: {time_2 - time_1}\tSave Image Time:{time_3 - time_2}")
finally:
    camera.release()
