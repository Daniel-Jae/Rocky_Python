# Own class for cameraOutput with own thread
# Only for debugging

import cv2
import numpy as np

# import concurrent.futures
from threading import Thread
import time


class VideoOutput:
    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            frame = cv2.resize(self.frame, (0, 0), fx=0.6, fy=0.6)
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True
