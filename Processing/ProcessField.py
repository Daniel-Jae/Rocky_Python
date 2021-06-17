# Gets Input(Image) from a VideoStream and transforms and warps the Image so that
# the resulting image has always the same dimensions and the robot- and human-line are on the same side
# The game-field in the image has to be put manually by calling chooseCorner()
# -> Left-MouseClick = Robot-Corner AND Right-MouseClick = Human-Corner
# After the corners have been selected you can choose wheter or not you want to flip the image (so far in the terminal)

import cv2
import numpy as np
import matplotlib.pyplot as plt

from constants import *

# import concurrent.futures
# import threading
# import time

# Test-Images
img = cv2.imread("Processing/field_TestImages/test_image.jpeg", 1)
img = cv2.resize(img, (0, 0), fx=0.7, fy=0.7)


class ProcessField:
    def __init__(self, videoStream=0):
        self.videostream = videoStream
        frame, amountOfFrames = self.videostream.read()
        # frame = cv2.resize(frame, (0, 0), fx=0.7, fy=0.7)
        self.image = frame
        self.ptHuman = []
        self.ptRobot = []

        # Points in the source image: Corners of the game-field
        self.pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])

        # Points(And therefore dimensions) for the destination-image.
        self.pts2 = np.float32([[0, 0], [640, 0], [0, 400], [640, 400]])

        self.height = int(self.pts2[3, 0])
        self.length = int(self.pts2[3, 1])
        self.pts2NotSuitable = np.float32([[0, 0], [400, 0], [0, 640], [400, 640]])
        # the amount of rotation(clock-wise)
        self.rotate = 0
        # True -> larger width than height (Goal-line left and right); False -> larger height than width (Goal-line top and bottom)
        self.suitableForm = True
        # True -> Flip Image vertically: Change left and right for robot
        self.flipImage = False

        self.choosenCorner = False

    def click_event(self, event, x, y, flags, param):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN and len(self.ptRobot) < 2:
            pt = [x, y]
            self.ptRobot.append(pt)
            print(self.ptRobot)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(
                self.image, "Roboter", (x + 10, y + 10), font, 0.9, (0, 0, 255), 2
            )
            # circle outside point
            cv2.circle(self.image, (x, y), 10, (0, 0, 255), 2)
            # point
            cv2.circle(self.image, (x, y), 2, (0, 0, 255), -1)
            cv2.imshow("image", self.image)

        # checking for right mouse clicks
        elif event == cv2.EVENT_RBUTTONDOWN and len(self.ptHuman) < 2:
            pt = [x, y]
            self.ptHuman.append(pt)
            print(self.ptHuman)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(
                self.image, "Mensch", (x + 10, y + 10), font, 0.9, (255, 0, 0), 2
            )
            # circle outside point
            cv2.circle(self.image, (x, y), 10, (255, 0, 0), 2)
            # point
            cv2.circle(self.image, (x, y), 2, (255, 0, 0), -1)
            cv2.imshow("image", self.image)

    def chooseCorner(self):
        # print(self.image)

        cv2.imshow("image", self.image)
        cv2.setMouseCallback("image", self.click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # height = self.image.shape[0]
        # width = self.image.shape[1]

        newList = []
        # the amount of rotation(clock-wise)
        self.rotate = 0
        # True -> larger width than height (Goal-line left and right); False -> larger height than width (Goal-line top and bottom)
        self.suitableForm = True
        # Check if the goal-lines are "left and right" or "top and bottom". If true: The difference between the x-values of the human and robot-line is bigger than the y-values. Therefore the lines are "left and right"
        if abs(
            (self.ptRobot[0][0] + self.ptRobot[1][0])
            - (self.ptHuman[0][0] + self.ptHuman[1][0])
        ) > abs(
            (self.ptRobot[0][1] + self.ptRobot[1][1])
            - (self.ptHuman[0][1] + self.ptHuman[1][1])
        ):
            # Check wheter robot is on the right or left side. If true: robot on the right side
            if (self.ptRobot[0][0] + self.ptRobot[1][0]) > (
                self.ptHuman[0][0] + self.ptHuman[1][0]
            ):
                # Check which point is on top: If true: first point on top
                if self.ptHuman[0][1] < self.ptHuman[1][1]:
                    newList.append(self.ptHuman[0])

                    if self.ptRobot[0][1] < self.ptRobot[1][1]:
                        newList.append(self.ptRobot[0])
                        newList.append(self.ptHuman[1])
                        newList.append(self.ptRobot[1])
                    else:
                        newList.append(self.ptRobot[1])
                        newList.append(self.ptHuman[1])
                        newList.append(self.ptRobot[0])
                else:
                    newList.append(self.ptHuman[1])

                    if self.ptRobot[0][1] < self.ptRobot[1][1]:
                        newList.append(self.ptRobot[0])
                        newList.append(self.ptHuman[0])
                        newList.append(self.ptRobot[1])
                    else:
                        newList.append(self.ptRobot[1])
                        newList.append(self.ptHuman[0])
                        newList.append(self.ptRobot[0])
            # robot on the left side
            else:
                self.rotate = 180
                # Check which point is on top: If true: first point on top
                if self.ptRobot[0][1] < self.ptRobot[1][1]:
                    newList.append(self.ptRobot[0])

                    if self.ptHuman[0][1] < self.ptHuman[1][1]:
                        newList.append(self.ptHuman[0])
                        newList.append(self.ptRobot[1])
                        newList.append(self.ptHuman[1])
                    else:
                        newList.append(self.ptHuman[1])
                        newList.append(self.ptRobot[1])
                        newList.append(self.ptHuman[0])
                else:
                    newList.append(self.ptRobot[1])

                    if self.ptHuman[0][1] < self.ptHuman[1][1]:
                        newList.append(self.ptHuman[0])
                        newList.append(self.ptRobot[0])
                        newList.append(self.ptHuman[1])
                    else:
                        newList.append(self.ptHuman[1])
                        newList.append(self.ptRobot[0])
                        newList.append(self.ptHuman[0])
        else:
            self.suitableForm = False
            # Check wheter robot is on the top or bottom. If true: robot on the top
            if (self.ptRobot[0][1] + self.ptRobot[1][1]) < (
                self.ptHuman[0][1] + self.ptHuman[1][1]
            ):
                self.rotate = 90
                if self.ptRobot[0][0] < self.ptRobot[1][0]:
                    newList.append(self.ptRobot[0])
                    newList.append(self.ptRobot[1])
                else:
                    newList.append(self.ptRobot[1])
                    newList.append(self.ptRobot[0])

                if self.ptHuman[0][0] < self.ptHuman[1][0]:
                    newList.append(self.ptHuman[0])
                    newList.append(self.ptHuman[1])
                else:
                    newList.append(self.ptHuman[1])
                    newList.append(self.ptHuman[0])
            # robot on bottom
            else:
                self.rotate = 270
                if self.ptHuman[0][0] < self.ptHuman[1][0]:
                    newList.append(self.ptHuman[0])
                    newList.append(self.ptHuman[1])
                else:
                    newList.append(self.ptHuman[1])
                    newList.append(self.ptHuman[0])

                if self.ptRobot[0][0] < self.ptRobot[1][0]:
                    newList.append(self.ptRobot[0])
                    newList.append(self.ptRobot[1])
                else:
                    newList.append(self.ptRobot[1])
                    newList.append(self.ptRobot[0])

        # Check form of img
        # if (width > height):
        # Check wheter robot is on the right or left side. If true: right side
        # if ((self.ptRobot[0][0] + self.ptRobot[1][0]) > (self.ptHuman[0][0] + self.ptHuman[1][0])):

        self.pts1 = np.asarray(newList, np.float32)
        print(self.pts1)

        """ test = np.asarray(self.ptRobot, np.float32)
        print(test)
        test2 = np.asarray(self.ptHuman, np.float32)
        print(test2)
        test3 = np.append(test, test2, axis=0)
        print(test3)
        print(self.pts1) """

        if self.suitableForm == False:
            self.pts2 = self.pts2NotSuitable

        self.height = int(self.pts2[3, 0])
        self.length = int(self.pts2[3, 1])

        M = cv2.getPerspectiveTransform(self.pts1, self.pts2)
        dst = cv2.warpPerspective(self.image, M, (self.height, self.length))

        if self.rotate == 180:
            dst = cv2.rotate(dst, cv2.cv2.ROTATE_180)
        elif self.rotate == 90:
            dst = cv2.rotate(dst, cv2.cv2.ROTATE_90_CLOCKWISE)
        elif self.rotate == 270:
            dst = cv2.rotate(dst, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

        plt.subplot(121), plt.imshow(self.image), plt.title("Input")
        plt.subplot(122), plt.imshow(dst), plt.title("Output")
        plt.show()

        # Answer wether or not you want to flip the camera-input vertically.
        # If you flip: left and right for the robot gets switched
        answerFlip = None
        while answerFlip not in ("J", "j", "n", "N"):
            answerFlip = input("Willst du das Bild spiegeln? (J/N): ")
            if answerFlip == "j" or answerFlip == "J":
                self.flipImage = True
                flippedDst = cv2.flip(dst, 0)
                plt.imshow(flippedDst), plt.title("Output")
                plt.show()
            elif answerFlip == "n" or answerFlip == "N":
                self.flipImage = False
            else:
                print("Bitte gebe (J/N) ein. J = Ja und N = Nein.")

        self.choosenCorner = True

    def getImage(self):
        # Because the flow of the programm doesn't use getImage() before chooseCorner() got called, this query is useless for now.
        """if self.chooseCorner == False:
            answerCorner = None
            while answerCorner not in ("J", "j", "n", "N"):
                answerCorner = input("Du hast noch keine Ecken für das Spielfeld ausgewählt. Mit dem ganzen Bild fortfahren? (J/N): ")
                if answerCorner == "j" or answerCorner == "J":
                    return self.videoStream.getImage()
                elif answerCorner == "n" or answerCorner == "N":
                    self.chooseCorner()
                else:
                    print("Bitte gebe (J/N) ein. J = Ja und N = Nein.")

        else:"""

        img, amountOfFrames = self.videostream.read()
        # if amountOfFrames == 0:
        #    return (0, 0)
        M = cv2.getPerspectiveTransform(self.pts1, self.pts2)
        dst = cv2.warpPerspective(img, M, (self.height, self.length))

        if self.rotate == 180:
            dst = cv2.rotate(dst, cv2.cv2.ROTATE_180)
        elif self.rotate == 90:
            dst = cv2.rotate(dst, cv2.cv2.ROTATE_90_CLOCKWISE)
        elif self.rotate == 270:
            dst = cv2.rotate(dst, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

        if self.flipImage == True:
            dst = cv2.flip(dst, 0)

        return (dst, amountOfFrames)


if __name__ == "__main__":
    pass

    test = ProcessField()
    test.chooseCorner()

    print("EXIT")
    exit
