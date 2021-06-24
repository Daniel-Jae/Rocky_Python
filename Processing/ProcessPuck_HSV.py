import cv2
import numpy as np
import matplotlib.pyplot as plt
from Camera.cameraOutput import VideoOutput

from Constants import constants


class ProcessPuckHSV:
    def __init__(self, processField=0):
        self.field = processField

        self.lower_boundary = np.array([61, 94, 40])
        self.upper_boundary = np.array([90, 255, 144])

    # callback-function for trackbar. We don't use it, but have to declare it
    def nothing(x, y):
        pass

    def setHSV(self):
        # make a trackbar with sliders for hsv lower and upper values. default values are derived from self.lower_ and upper_boundary
        cv2.namedWindow("SetHSV")
        cv2.createTrackbar(
            "Lower_Hue",
            "SetHSV",
            self.lower_boundary[0].item(),
            255,
            self.nothing,
        )
        cv2.createTrackbar(
            "Lower_Saturation",
            "SetHSV",
            self.lower_boundary[1].item(),
            255,
            self.nothing,
        )
        cv2.createTrackbar(
            "Lower_Value",
            "SetHSV",
            self.lower_boundary[2].item(),
            255,
            self.nothing,
        )
        cv2.createTrackbar(
            "Upper_Hue",
            "SetHSV",
            self.upper_boundary[0].item(),
            255,
            self.nothing,
        )
        cv2.createTrackbar(
            "Upper_Saturation",
            "SetHSV",
            self.upper_boundary[1].item(),
            255,
            self.nothing,
        )
        cv2.createTrackbar(
            "Upper_Value",
            "SetHSV",
            self.upper_boundary[2].item(),
            255,
            self.nothing,
        )

        # "while True", so that the images are getting "refreshed" everytime the hsv values change
        while True:
            img = self.getImage()
            if not img:
                continue

            img = cv2.resize(img, (0, 0), fx=0.1, fy=0.1)

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # get value from Trackbar. We use this instead of 6 different callback-functions
            l_h = cv2.getTrackbarPos("Lower_Hue", "SetHSV")
            l_s = cv2.getTrackbarPos("Lower_Saturation", "SetHSV")
            l_v = cv2.getTrackbarPos("Lower_Value", "SetHSV")
            u_h = cv2.getTrackbarPos("Upper_Hue", "SetHSV")
            u_s = cv2.getTrackbarPos("Upper_Saturation", "SetHSV")
            u_v = cv2.getTrackbarPos("Upper_Value", "SetHSV")

            # set new boundaries
            self.lower_boundary = np.array([l_h, l_s, l_v])
            self.upper_boundary = np.array([u_h, u_s, u_v])

            mask = cv2.inRange(hsv, self.lower_boundary, self.upper_boundary)

            res = cv2.bitwise_and(img, img, mask=mask)

            cv2.imshow("image", img)
            cv2.imshow("mask", mask)
            cv2.imshow("result", res)
            key = cv2.waitKey(1)
            # ESC
            if key == 27:
                break

        cv2.destroyAllWindows()

    def getPuckPosition(self):
        # img = self.getImage()
        img, amountOfFrames = self.field.getImage()
        if amountOfFrames == 0:
            return ((0, 0), 0)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.lower_boundary, self.upper_boundary)

        # We use medianBlur to get rid of so calles salt and pepper noise.
        # If our mask gets other pixels besides the puck, we hope to eliminate them as best as possible with this "filter"
        mask_blur = cv2.medianBlur(mask, 19)

        contours, hierarchy = cv2.findContours(mask_blur, 1, 2)

        if not contours:
            return ((0, 0), 0)

        cnt = contours[0]

        # We use minEnclosingCircle(), because if part of the puck is not detected (perhaps an arm above the puck), we might still be
        # able to get the correct center
        # We also tried cv2.HoughCircles as seen in "testHSV.py", but somehow it doesn't work.
        # It might be faster than this method though. So if you are able to get the center with cv2.HoughCircles... give it a try
        # (x, y), radius = cv2.minEnclosingCircle(cnt)
        # center = (int(x), int(y))

        M = cv2.moments(cnt)
        # Check for null-divison
        if M["m00"] == 0:
            return ((0, 0), 0)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        center = (cx, cy)
        # print(center)
        return (center, amountOfFrames)

    def getPuckPositionAlways(self):
        # img = self.getImage()
        img, amountOfFrames = self.field.getImage()
        while amountOfFrames == 0:
            img, amountOfFrames = self.field.getImage()
        video_shower = VideoOutput(img).start()

        # img = cv2.imread("Processing/hsv_TestImages/hsv_test_1.jpeg", 1)
        while True:
            if cv2.waitKey(1) == ord("q"):
                break

            img, amountOfFrames = self.field.getImage()
            if amountOfFrames == 0:
                continue
            # print(amountOfFrames)

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, self.lower_boundary, self.upper_boundary)

            # We use medianBlur to get rid of so calles salt and pepper noise.
            # If our mask gets other pixels besides the puck, we hope to eliminate them as best as possible with this "filter"
            mask_blur = cv2.medianBlur(mask, 19)

            contours, hierarchy = cv2.findContours(mask_blur, 1, 2)
            if not contours:
                video_shower.frame = img
                continue
            cnt = contours[0]

            # We use minEnclosingCircle(), because if part of the puck is not detected (perhaps an arm above the puck), we might still be
            # able to get the correct center
            # We also tried cv2.HoughCircles as seen in "testHSV.py", but somehow it doesn't work.
            # It might be faster than this method though. So if you are able to get the center with cv2.HoughCircles... give it a try

            M = cv2.moments(cnt)
            # Check for null-divison
            if M["m00"] == 0:
                video_shower.frame = img
                continue
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            center = (cx, cy)

            # (x, y), radius = cv2.minEnclosingCircle(cnt)
            # center = (int(x), int(y))

            print(center)

            cv2.circle(img, center, 20, (255, 0, 0), 2)
            video_shower.frame = img

        video_shower.stop()
        return (center, amountOfFrames)

    # Get the correct (only the field) image from ProcessField
    def getImage(self):
        # img = cv2.imread("Processing/hsv_TestImages/hsv_test_1.jpeg", 1)
        img, amountOfFrames = self.field.getImage()
        if amountOfFrames == 0:
            return None
        return img

    def read_position_and_image(self):
        img, amountOfFrames = self.field.getImage()
        if amountOfFrames == 0:
            return (img, (0, 0), 0)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_boundary, self.upper_boundary)

        # We use medianBlur to get rid of so calles salt and pepper noise.
        # If our mask gets other pixels besides the puck, we hope to eliminate them as best as possible with this "filter"
        mask_blur = cv2.medianBlur(mask, 19)

        contours, hierarchy = cv2.findContours(mask_blur, 1, 2)

        if not contours:
            return ((0, 0), 0)

        cnt = contours[0]

        M = cv2.moments(cnt)
        # Check for null-divison
        if M["m00"] == 0:
            return ((0, 0), 0)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        center = (cx, cy)
        # print(center)
        return (img, center, amountOfFrames)


if __name__ == "__main__":
    pass

    test = ProcessPuckHSV()
    test.setHSV()
    position = test.getPuckPositionAlways()
    print(position)

    print("EXIT")
    exit
