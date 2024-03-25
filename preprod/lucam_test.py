from lucam import Lucam
camera = Lucam()
image = camera.TakeSnapshot()
camera.SaveImage(image, 'test.tif')
camera.CameraClose()