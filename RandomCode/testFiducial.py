import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

# import constants

from Constants import constants

# import imutils
import sys

img = cv2.imread("Processing/fiducial_TestImages/fid_test_7.jpeg", 1)
img = cv2.resize(img, (0, 0), fx=0.7, fy=0.7)

blurred = cv2.medianBlur(img, 3)
cv2.imshow("test", blurred)
cv2.waitKey(0)

img = blurred

# define names of each possible ArUco tag OpenCV support


arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(
    img, arucoDict, parameters=arucoParams
)


id = 0

# verify *at least* one ArUco marker was detected
if len(corners) > 0 and (constants.PUCK_ARUCO_ID in ids):
    # flatten the ArUco IDs list
    ids = ids.flatten()
    # loop over the detected ArUCo corners
    for (markerCorner, markerID) in zip(corners, ids):
        # extract the marker corners (which are always returned in
        # top-left, top-right, bottom-right, and bottom-left order)
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))

        # draw the bounding box of the ArUCo detection
        cv2.line(img, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 2)
        # compute and draw the center (x, y)-coordinates of the ArUco
        # marker
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
        # draw the ArUco marker ID on the img
        cv2.putText(
            img,
            str(markerID),
            (topLeft[0], topLeft[1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )
        print("[INFO] ArUco marker ID: {}".format(markerID))
        # show the output img
        cv2.imshow("img", img)
        cv2.waitKey(0)
