import cv2
import math
import numpy as np
from Camera.cameraOutput import VideoOutput

from Constants import constants


class PathPredictionTest:
    def __init__(self, processPuckHSV=0):
        self.getPuck = processPuckHSV
        self.center_old, self.center_new = np.array([0, 0])
        self.time_between = 0

    # calculate speed in ??????????
    def calculateSpeed(self, center1, center2, time):
        # x1, y1 = center1
        # x2, y2 = center2
        distance = math.sqrt(
            (center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2
        )
        return distance / time

    # Examples: (3/1), (1/6), (1/1), (1.2/1)
    def calculateDirection(center1, center2):
        distanceX = center2[0] - center1[0]
        distanceY = center2[1] - center1[1]
        if distanceX == 0 or distanceY == 0:
            return (distanceX, distanceY)
        elif distanceX > distanceY:
            return (distanceX / abs(distanceY), distanceY / abs(distanceY))
        else:
            return (distanceX / abs(distanceX), distanceY / abs(distanceX))

    # calculate speed in ??????????
    def calculateSpeedNumpy(center1, center2, time):
        # x1, y1 = center1
        # x2, y2 = center2
        distance = math.sqrt(
            (center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2
        )
        return distance / time

    # Return vector with length of one
    def calculateDirectionNumpy(center1, center2):
        # centers must be np.arrays. example: np.array([420, 69])
        diff = center2 - center1

        # lowest value of vector -> np.linalg.norm(diffs, -np.inf)
        # length of vector -> np.linalg.norm(diffs)... at least in our 1-D Array
        normalized_vector = diff / np.linalg.norm(diff)

        return normalized_vector


if __name__ == "__main__":

    print("EXIT")
    exit
