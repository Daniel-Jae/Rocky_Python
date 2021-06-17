import cv2
import numpy as np

# import concurrent.futures
import time


class CameraCalibration:
    def __init__(self, chessboard=(9, 6), camera=0):
        # initialize the camera and stream
        self.camera = camera
        # self.resolution = resolution
        self.chessboardSize = chessboard
        self.images = []

    def calibrate(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros(
            (self.chessboardSize[0] * self.chessboardSize[1], 3), np.float32
        )
        objp[:, :2] = np.mgrid[
            0 : self.chessboardSize[0], 0 : self.chessboardSize[1]
        ].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.

        for fname in self.images:
            gray = cv2.cvtColor(fname, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (self.chessboardSize), None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)
                # Draw and display the corners
                cv2.drawChessboardCorners(fname, (self.chessboardSize), corners2, ret)
                cv2.imshow("img", fname)
                cv2.waitKey(500)
        cv2.destroyAllWindows()

    def showImages(self):
        for fname in self.images:
            cv2.imshow("img", fname)
            cv2.waitKey(300)

    def getImages(self):
        cap = cv2.VideoCapture(self.camera)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        for x in range(20):
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame!")
                break
            # Our operations on the frame come here
            self.images.append(frame)

            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == ord("q"):
                break
            time.sleep(5)
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

        pass


if __name__ == "__main__":
    pass

    video = CameraCalibration()
    video.getImages()
    video.showImages()
    video.calibrate()
