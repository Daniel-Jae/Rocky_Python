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

    def saveParameter(self):
        pass

    def showUndistortImage(self):
        dst = cv2.undistort(
            self.images[0], self.cameraMatrix, self.distortion, None, self.newcameramtx
        )
        # crop the image
        x, y, w, h = self.roi
        dst = dst[y : y + h, x : x + w]
        cv2.imshow("calibresult.png", dst)
        cv2.waitKey(0)

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

                drawCorners = fname.copy()
                cv2.drawChessboardCorners(
                    drawCorners, (self.chessboardSize), corners2, ret
                )
                cv2.imshow("img", drawCorners)
                cv2.waitKey(500)
        cv2.destroyAllWindows()

        ret, self.cameraMatrix, self.distortion, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None
        )

        mean_error = 0
        for i in range(len(objpoints)):
            imgpoints2, _ = cv2.projectPoints(
                objpoints[i], rvecs[i], tvecs[i], self.cameraMatrix, self.distortion
            )
            error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
            mean_error += error
        print("total error: {}".format(mean_error / len(objpoints)))

        h, w = gray.shape[:2]
        self.newcameramtx, self.roi = cv2.getOptimalNewCameraMatrix(
            self.cameraMatrix, self.distortion, (w, h), 1, (w, h)
        )

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
    video.showUndistortImage()
