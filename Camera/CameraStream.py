import cv2
import numpy as np

# import concurrent.futures
from threading import Thread
import time


class VideoStream:
    def __init__(self, camera=0, framerate=60, calibration=None):
        self.stream = cv2.VideoCapture(camera)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.framesSinceLastRequest = 0
        self.framerate = framerate
        self.camera_calibration = calibration
        if self.camera_calibration != None:
            self.camera_calibration.choose()

        self.currentTime = time.time()
        self.previousTime = time.time()

    def calculateFPS():
        # Calculate the "real" Frames of the Camera
        video = cv2.VideoCapture(0)
        # Number of frames to capture
        num_frames = 120

        start = time.time()

        # Grab a few frames
        for _ in range(0, num_frames):
            video.read()

        end = time.time()

        seconds = end - start
        fps = num_frames / seconds
        video.release()

        return fps

    def start(self):
        self.previousTime = time.time()
        if self.camera_calibration == None:
            Thread(target=self.get_without_calibration, args=()).start()
            return self
        elif self.camera_calibration.getCalibration() == None:
            Thread(target=self.get_without_calibration, args=()).start()
            return self
        else:
            (
                self.cameraMatrix,
                self.distortion,
            ) = self.camera_calibration.getCalibration()
            Thread(target=self.get_with_calibration, args=()).start()
            return self

    def get_without_calibration(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                self.framesSinceLastRequest += 1
                (self.grabbed, self.frame) = self.stream.read()
        print("Camera stopped.")

    def get_with_calibration(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                self.framesSinceLastRequest += 1
                (self.grabbed, self.frame) = self.stream.read()
                h, w = self.frame.shape[:2]
                self.newcameramtx, self.roi = cv2.getOptimalNewCameraMatrix(
                    self.cameraMatrix, self.distortion, (w, h), 1, (w, h)
                )
                self.frame = cv2.undistort(
                    self.frame,
                    self.cameraMatrix,
                    self.distortion,
                    None,
                    self.newcameramtx,
                )
        print("Camera stopped.")

    # return the newest frame -if available- and return the amount of time -in seconds- that passed since the last request
    def readWithTime(self):
        framesSinceLastRequest = self.framesSinceLastRequest

        if framesSinceLastRequest == 0:
            return (self.frame, framesSinceLastRequest)
        else:
            self.currentTime = time.time()
            timeSinceLastRequest = self.currentTime - self.previousTime
            self.previousTime = self.currentTime

            self.framesSinceLastRequest = 0

            return (self.frame, timeSinceLastRequest)

    # return the newest frame -if available- and return the amount of frames that passed since the last request
    def readWithFrames(self):
        framesSinceLastRequest = self.framesSinceLastRequest

        if framesSinceLastRequest == 0:
            return (self.frame, framesSinceLastRequest)
        else:
            self.framesSinceLastRequest = 0

            return (self.frame, framesSinceLastRequest)

    def stop(self):
        self.stopped = True
        self.newFrame = False
        self.frame = None


def show(source=0):

    video_getter = VideoStream(camera=source).start()

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

        frame, amountOfFrames = video_getter.read()
        if amountOfFrames == 0:
            continue
        print(amountOfFrames)
        cv2.imshow("Video", frame)


if __name__ == "__main__":
    pass

    show(0)
    # video = VideoStream()
    # video.start()
