import cv2

class Camera:

    def __init__(self, video):
        self.__video = video
        self.__cap = cv2.VideoCapture(video)

    def read(self):
        ret, frame = self.__cap.read()
        if ret == True:
            return frame
        else:
            print(ret)
            self.__cap = cv2.VideoCapture(self.__video)
            return self.read()