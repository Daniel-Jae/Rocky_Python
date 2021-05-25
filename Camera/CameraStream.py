import cv2
import numpy as np

# import concurrent.futures
import threading
import time


class VideoStream:
    def __init__(self, resolution=(320, 240), framerate=60, camera=0):
        # initialize the camera and stream
        self.camera = camera
        self.resolution = resolution
        self.framerate = framerate
        self.realFramerate = framerate
        # time between frames in milliseconds
        ### self.timePerFrame = 1000 / framerate
        self.framesSinceLastRequest = 0

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = True

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
        # start the thread to read frames from the video stream
        if self.stopped:
            self.stopped = False
            t1 = threading.Thread(target=self.update)
            t1.start()
            # Potentielle Alternativen
            # 1
            # add "t1.daemon = True" before "t1.start()"
            # 2
            # thread_pool = concurrent.futures.ThreadPoolExecutor()
            # thread_pool.submit(self.update)

            return self

    def update(self):
        # get always a new picture as long as the thread is still alive
        video = cv2.VideoCapture(self.camera)
        if not video.isOpened():
            print("Cannot open camera")
            return
        try:
            while True:
                # grab the frame from the stream and clear the stream in
                # preparation for the next frame
                ret, frame = video.read()
                # ret checks if you could actually get a frame
                if ret:
                    self.frame = frame
                self.newFrame = True
                self.framesSinceLastRequest += 1

                # if the thread indicator variable is set, stop the thread
                # and resource camera resources
                if self.stopped:
                    video.release()
                    print("Camera stopped.")
                    return
        except:
            self.frame = None

    def read(self):
        # return the newest frame
        self.newFrame = False
        self.framesSinceLastRequest = 0
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        self.newFrame = False
        self.frame = None
        self.counter.stop()


if __name__ == "__main__":
    pass

    video = VideoStream()
    video.start()
