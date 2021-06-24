import cv2
import numpy as np

# import concurrent.futures
from threading import Thread
import time


class VideoStream:
    def __init__(self, camera=0, framerate=60):
        self.stream = cv2.VideoCapture(camera)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        self.framesSinceLastRequest = 0
        self.framerate = framerate

        self.currentTime, self.previousTime = 0

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
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                self.framesSinceLastRequest += 1
                (self.grabbed, self.frame) = self.stream.read()
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
