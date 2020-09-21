import cv2
import numpy as np

class ParkingRois:

    def __init__(self):
        self.__corners = []
        self.__parking_contours = []
        self.__parking_contours_np = []
        self.__ready = False

    def print_parking_rois(self, frame):
        if len(self.__corners) > 0:
            print("Need circle")
            print(len(self.__corners))
            for i in range(len(self.__corners)):
                cv2.circle(frame, (self.__corners[i]), 5, (255, 0, 0), -1)

        if len(self.__parking_contours) > 0:
            for parking_contour in self.__parking_contours:
                for i in range(len(parking_contour) - 1):
                    cv2.line(frame, parking_contour[i], parking_contour[i + 1], (255, 0, 0), 1)
                cv2.line(frame, parking_contour[3], parking_contour[0], (255, 0, 0), 1)

        return frame

    def create_parking_rois(self):
        cv2.setMouseCallback("Main_roi", self.__create_parking_contours_mouse_event)

    def __create_parking_contours_mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.__corners) < 4:
                self.__corners.append((x, y))
            if len(self.__corners) == 4:
                self.__parking_contours.append(self.__corners)
                self.__corners = []
        if event == cv2.EVENT_RBUTTONDOWN:
            self.__parking_contours_np = np.array([self.__parking_contours])
            self.__ready = True

    @property
    def get_ready(self):
        return self.__ready

    def get_final_frame(self, frame):
        print("final step")