import cv2
import numpy as np

class Contours:

    def __init__(self):
        self.__frame = None
        self.__main_contour = []
        self.__main_contour_np = np.array([])
        self.__ready_to_crop = False

    def print_main_contour(self, frame):
        self.__frame = frame
        if len(self.__main_contour) > 0:
            for i in range(len(self.__main_contour)):
                cv2.circle(frame, (self.__main_contour[i]), 5, (255, 0, 0), -1)

        if len(self.__main_contour) > 1:
            for i in range(len(self.__main_contour) - 1):
                cv2.line(frame, self.__main_contour[i], self.__main_contour[i + 1], (255, 0, 0), 1)

        return frame

    def create_main_contour(self):
        cv2.setMouseCallback("Src", self.__create_main_contour_mouse_event)

    def __create_main_contour_mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__main_contour.append((x, y))
        if event == cv2.EVENT_RBUTTONDOWN:
            self.__main_contour_np = np.array([self.__main_contour])
            self.__ready_to_crop = True

    @property
    def get_ready_to_crop(self):
        return self.__ready_to_crop

    def crop_and_mask_main_contour(self, frame):
        mask = np.zeros(frame.shape[0:2], dtype=np.uint8)
        cv2.drawContours(mask, [self.__main_contour_np], -1, (255, 255, 255), -1, cv2.LINE_AA)

        res = cv2.bitwise_and(frame, frame, mask=mask)
        rect = cv2.boundingRect(self.__main_contour_np)  # returns (x,y,w,h) of the rect
        cropped = res[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]

        wbg = np.ones_like(cropped, np.uint8) * 255
        # cv2.bitwise_not(wbg, wbg)
        dst = wbg + cropped

        return dst