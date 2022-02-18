import urllib
import cv2
import numpy as np

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    print("Warning - Could not import picamera module")


class Camera(object):
    def __init__(self, url=None, file=None):
        self.url = url
        self.file = file
        if url is None and file is None:
            self.camera = PiCamera()
            self.camera.resolution = (1024, 768)
            self.rawCapture = PiRGBArray(self.camera)

    def shutwodn(self):
        if self.camera:
            self.camera.close()

    def grab_frame(self):
        if self.url:
            response = urllib.request.urlopen(self.url)
            data = response.read()
            return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        if self.file:
            return cv2.imread(self.file)
        # use the picam directly
        self.camera.capture(self.rawCapture, format="bgr")
        return self.rawCapture.array
