from pixelink import PixeLINK
from PIL import Image
cam = PixeLINK()
cam.shutter = 0.002
#print(cam.grab())
result = None
result = cam.grab()
print(result.mean())
im = Image.fromarray(result)
im.save('test0.png')
cam.shutter = 0.003
raw_data = cam.grab()
print(raw_data.mean())
cam.close()

im = Image.fromarray(raw_data)
im.save('test1.png')
