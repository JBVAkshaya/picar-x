from re import L
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)

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
        lower_blue = np.array([h_lower, 50, 50])
        upper_blue = np.array([h_upper, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        edges = cv2.Canny(mask, 200, 400)
        line_edges = self.region_of_interest(edges)
        return bgr, mask, line_edges
    
    def make_points(self, line):
        (height, width) = self.camera.resolution
        slope, intercept = line
        y1 = height  # bottom of the frame
        y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

        # bound the coordinates within the frame
        x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
        x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
        return [[x1, y1, x2, y2]]

    def detect_line_segments(self, line_edges):
        # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
        rho = 1  # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
        min_threshold = 10  # minimal of votes
        line_segments = cv2.HoughLinesP(line_edges, rho, angle, min_threshold, 
                                        np.array([]), minLineLength=8, maxLineGap=4)

        return line_segments
    
    def average_slope_intercept(self, line_segments):
        """
        This function combines line segments into one or two lane lines
        If all line slopes are < 0: then we only have detected left lane
        If all line slopes are > 0: then we only have detected right lane
        """
        lane_lines = []
        if line_segments is None:
            logging.info('No line_segment segments detected')
            return lane_lines

        # height, width, _ = frame.shape
        # left_fit = []
        # right_fit = []
        fit = []

        # boundary = 1/3
        # left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
        # right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

        for line_segment in line_segments:
            for x1, y1, x2, y2 in line_segment:
                # if x1 == x2:
                #     logging.info('skipping vertical line segment (slope=inf): %s' % line_segment)
                #     continue
                # fit = np.polyfit((x1, x2), (y1, y2), 1)
                # slope = fit[0]
                # intercept = fit[1]
                # if slope < 0:
                #     if x1 < left_region_boundary and x2 < left_region_boundary:
                #         left_fit.append((slope, intercept))
                # else:
                #     if x1 > right_region_boundary and x2 > right_region_boundary:
                #         right_fit.append((slope, intercept))
                slope, intercept = np.polyfit((x1, x2), (y1, y2), 1)
                logging.debug(f"slope, intercept: {slope, intercept}")
                fit.append((slope,intercept))

        fit_average = np.median(fit, axis=0)
        logging.debug(f"len fit, fit avg: {len(fit), fit_average}")
        if len(fit) > 0:
            lane_lines.append(self.make_points(fit_average))

        # right_fit_average = np.average(right_fit, axis=0)
        # if len(right_fit) > 0:
        #     lane_lines.append(make_points(frame, right_fit_average))

        logging.debug('lane lines: %s' % lane_lines)  # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]

        return lane_lines

    def detect_lane(self, frame):
        bgr, mask, edges = self.get_line_edges(frame)
        line_segments = self.detect_line_segments(edges)
        logging.debug(f"all line segments: {line_segments}")
        lane_lines = self.average_slope_intercept(line_segments)
        return bgr, mask, edges, lane_lines
    
    def display_lines(frame, lines, line_color=(0, 255, 0), line_width=2):
        line_image = np.zeros_like(frame)
        logging.debug(f"lines: {lines}")
        logging.debug(f"line cord: {lines[0][0]}")
        x1,y1,x2,y2 = lines[0][0]
        # if lines is not None:
        #     for line in lines:
        #         for x1, y1, x2, y2 in line:
        cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
        line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        return line_image

if __name__=="__main__":
    cam = Camera()
    for frame in cam.camera.capture_continuous(cam.rawCapture, format="bgr",use_video_port=True):
        try:
            bgr, mask, edges, lines = cam.detect_lane(frame.array)
            logging.debug(f"lines: {lines}")
            # logging.debug(f"line cord: {lines[0][0]}")
            # 
            cv2.imshow("video", bgr)
            cv2.imshow("mask", mask)
            cv2.imshow("lines", edges)
            # logging.debug(df"{lines}")
            # line_image = cam.display_lines(bgr,lines)
            # cv2.imshow("edges", line_image)
            cam.rawCapture.truncate(0)
            k = cv2.waitKey(1) & 0xFF
            # 27 is the ESC key, which means that if you press the ESC key to exit
            if k == 27:
                cam.camera.close()
                break
        except:
            logging.debug("faulty frame")
            continue