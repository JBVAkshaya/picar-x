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

    def region_of_interest(self, edges):
        height, width = edges.shape
        mask = np.zeros_like(edges)

        # only focus bottom half of the screen
        polygon = np.array([[
            (0, height * 2.2 / 3),
            (width, height * 2.2 / 3),
            (width, height),
            (0, height),
        ]], np.int32)

        cv2.fillPoly(mask, polygon, 255)
        cropped_edges = cv2.bitwise_and(edges, mask)
        return cropped_edges

    def get_line_edges(self, bgr, h_lower = 60, h_upper = 150):
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([h_lower, 100, 100])
        upper_blue = np.array([h_upper, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        edges = cv2.Canny(mask, 200, 400)
        line_edges = self.region_of_interest(edges)
        return bgr, mask, line_edges

if __name__=="__main__":
    cam = Camera()
    for frame in cam.camera.capture_continuous(cam.rawCapture, format="bgr",use_video_port=True):
        bgr, mask, edges = cam.get_line_edges(frame.array)
        cv2.imshow("video", bgr)
        cv2.imshow("mask", mask)
        cv2.imshow("edges", edges)
        cam.rawCapture.truncate(0)
        k = cv2.waitKey(1) & 0xFF
        # 27 is the ESC key, which means that if you press the ESC key to exit
        if k == 27:
            cam.camera.close()
            break