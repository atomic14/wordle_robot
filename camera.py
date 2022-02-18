import urllib
import cv2
import numpy as np

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    print("Warning - Could not import picamera module")


def grab_frame(url=None, file=None):
    if url:
        response = urllib.request.urlopen(url)
        data = response.read()
        return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if file:
        return cv2.imread(file)
    # use the picam directly
    camera = PiCamera()
    camera.resolution = (1024, 768)
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array
    camera.close()
