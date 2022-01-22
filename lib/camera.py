import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np

class Camera(object):
    def __init__(self, resolution=(640,480), framerate=24):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution) 

    def get_line_edges(self, bgr, h_lower = 60, h_upper = 150):
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([h_lower, 40, 40])
        upper_blue = np.array([h_upper, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        edges = cv2.Canny(mask, 200, 400)
        # line_edges = 
        return bgr, mask, edges

if __name__=="__main__":
    cam = Camera()
    for frame in cam.camera.capture_continuous(cam.rawCapture, format="bgr",use_video_port=True):
        img = frame.array
        cv2.imshow("video", img)
        cam.rawCapture.truncate(0)
        k = cv2.waitKey(1) & 0xFF
        # 27 is the ESC key, which means that if you press the ESC key to exit
        if k == 27:
            cam.camera.close()
            break