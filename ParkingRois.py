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
        cropped = {}

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_min = np.array((0, 0, 0), np.uint8)
        hsv_max = np.array((254, 254, 254), np.uint8)
        thresh = cv2.inRange(hsv, hsv_min, hsv_max)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for park in self.__parking_contours_np:
            x, y, h, w = cv2.boundingRect(park)
            crop = frame[y: y + h, x: x + w]
            key = tuple((x, y, h, w))
            cropped.update({key: crop})

        cv2.drawContours(frame, contours, -1, (155, 255, 0), -1, cv2.LINE_AA)

        # for park in cropped.keys():
        # #     frame[park[0], park[1]] = cropped.get(park)
        #     cv2.imshow(park, cropped.get(park))

        cv2.imshow("Result", frame)