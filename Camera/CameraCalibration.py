import cv2
import numpy as np

# import concurrent.futures
import time


class CameraCalibration:
    def __init__(self, chessboard=(7, 6), camera=0):
        # initialize the camera and stream
        self.camera = camera
        # self.resolution = resolution
        self.chessboardSize = chessboard
        self.images = []

    def showImages(self):
        for fname in self.images:
            img = cv2.imread(fname)
            cv2.imshow("img", img)
            cv2.waitKey(500)

    def getImages(self):
        cap = cv2.VideoCapture(self.camera)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame!")
                break
            # Our operations on the frame come here
            self.images.append(frame)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv2.imshow("frame", gray)
            if cv2.waitKey(1) == ord("q"):
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

        pass


if __name__ == "__main__":
    pass

    video = CameraCalibration()
    video.getImages()
    video.showImages()
