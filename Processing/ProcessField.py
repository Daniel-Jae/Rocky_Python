import cv2
import numpy as np
import matplotlib.pyplot as plt


# import concurrent.futures
import threading
import time

img = cv2.imread("Processing/test_image.jpeg", 1)
img = cv2.resize(img, (0, 0), fx=0.7, fy=0.7)


class ProcessField:
    def __init__(self):
        # initialize the camera and stream
        # self.videostream = videoStream
        # self.image = videoStream.getImage
        self.image = img
        self.ptHuman = []
        self.ptRobot = []
        self.pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])

        self.pts2 = np.float32([[0, 0], [640, 0], [0, 400], [640, 400]])

        self.height = int(self.pts2[3, 0])
        self.length = int(self.pts2[3, 1])
        self.pts2NotSuitable = np.float32([[0, 0], [400, 0], [0, 640], [400, 640]])
        # the amount of rotation(clock-wise)
        self.rotate = 0
        # True -> larger width than height (Goal-line left and right); False -> larger height than width (Goal-line top and bottom)
        self.suitableForm = True

        # cv2.setMouseCallback('Set Corner', self.click_event)

    def click_event(self, event, x, y, flags, param):
        # checking for left mouse clicks
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.ptRobot) >= 2:
                return
            pt = [x, y]
            self.ptRobot.append(pt)
            print(self.ptRobot)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, "Roboter", (x + 10, y + 10), font, 0.9, (0, 0, 255), 2)
            # circle outside point
            cv2.circle(img, (x, y), 10, (0, 0, 255), 2)
            # point
            cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
            cv2.imshow("image", img)

        # checking for right mouse clicks
        if event == cv2.EVENT_RBUTTONDOWN:
            if len(self.ptHuman) >= 2:
                return
            pt = [x, y]
            self.ptHuman.append(pt)
            print(self.ptHuman)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, "Mensch", (x + 10, y + 10), font, 0.9, (255, 0, 0), 2)
            # circle outside point
            cv2.circle(img, (x, y), 10, (255, 0, 0), 2)
            # point
            cv2.circle(img, (x, y), 2, (255, 0, 0), -1)
            cv2.imshow("image", img)

    def chooseCorner(self):
        print(self.image)
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


if __name__ == "__main__":
    pass

    test = ProcessField()
    test.chooseCorner()

    print("EXIT")
    exit
