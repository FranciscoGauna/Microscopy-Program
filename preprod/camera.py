import cv2
from sys import getsizeof
from PIL import Image
from datetime import datetime


def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr


print(returnCameraIndexes())
exit(0)

camera = cv2.VideoCapture(0)
time_0 = datetime.now()
raw_data = camera.read()[1]
try:
    if raw_data:
        time_1 = datetime.now()
        image = Image.fromarray(raw_data)
        time_2 = datetime.now()
        with open("test.png", "wb+") as file:
            image.save(file, "png")
        time_3 = datetime.now()
        print(f"Read Camera Rime: {time_1 - time_0}\tCreate Image Time: {time_2 - time_1}\tSave Image Time:{time_3 - time_2}")
    else:
        print("no data :(")
finally:
    camera.release()
