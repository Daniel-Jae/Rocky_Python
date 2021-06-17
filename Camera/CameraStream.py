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

    def read(self):
        # return the newest frame
        framesSinceLastRequest = self.framesSinceLastRequest

        self.framesSinceLastRequest = 0

        # cv2.imshow("image", self.frame)

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
