import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse


def nothing(x):
    pass


cv2.namedWindow("Tracking")
cv2.createTrackbar("Lower_Hue", "Tracking", 61, 255, nothing)
cv2.createTrackbar("Lower_Saturation", "Tracking", 94, 255, nothing)
cv2.createTrackbar("Lower_Value", "Tracking", 40, 255, nothing)
cv2.createTrackbar("Upper_Hue", "Tracking", 90, 255, nothing)
cv2.createTrackbar("Upper_Saturation", "Tracking", 255, 255, nothing)
cv2.createTrackbar("Upper_Value", "Tracking", 144, 255, nothing)


test = cv2.imread("Processing/hsv_TestImages/hsv_test_1.jpeg", 1)
# test = cv2.resize(test, (0, 0), fx=0.3, fy=0.3)
onlyCircle = test.copy()
masktest = test.copy()


while True:
    img = cv2.imread("Processing/hsv_TestImages/hsv_test_1.jpeg", 1)
    # img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)
    output = img.copy()

    # cv2.imshow("test", img)
    # cv2.waitKey(0)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("Lower_Hue", "Tracking")
    l_s = cv2.getTrackbarPos("Lower_Saturation", "Tracking")
    l_v = cv2.getTrackbarPos("Lower_Value", "Tracking")
    u_h = cv2.getTrackbarPos("Upper_Hue", "Tracking")
    u_s = cv2.getTrackbarPos("Upper_Saturation", "Tracking")
    u_v = cv2.getTrackbarPos("Upper_Value", "Tracking")

    lower_boundary = np.array([l_h, l_s, l_v])
    upper_boundary = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_boundary, upper_boundary)

    res = cv2.bitwise_and(img, img, mask=mask)
    onlyCircle = res
    masktest = mask

    cv2.imshow("img", img)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)
    key = cv2.waitKey(1)
    if key == 27:
        break

# cv2.destroyAllWindows()


hough_circle = onlyCircle.copy()
cv2.imshow("circle", onlyCircle)
key = cv2.waitKey(0)

gray = cv2.cvtColor(onlyCircle, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(gray, 30, 255, 0)
cv2.imshow("gray", gray)
key = cv2.waitKey(0)

gray_bl = cv2.medianBlur(gray, 19)

cv2.imshow("blur", gray_bl)
key = cv2.waitKey(0)

ret, thresh = cv2.threshold(gray_bl, 30, 255, 0)

cv2.imshow("thresh", thresh)
key = cv2.waitKey(0)

cv2.imshow("mask", masktest)
key = cv2.waitKey(0)

mask_bl = cv2.medianBlur(masktest, 19)

cv2.imshow("mask_blur", mask_bl)
key = cv2.waitKey(0)

contours, hierarchy = cv2.findContours(mask_bl, 1, 2)
cnt = contours[0]
M = cv2.moments(cnt)
print(M)
cx = int(M["m10"] / M["m00"])
cy = int(M["m01"] / M["m00"])
print(cx)
print(cy)

# im2, contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnt = contours[0]
(x, y), radius = cv2.minEnclosingCircle(cnt)
center = (int(x), int(y))
radius = int(radius)
print(center)
print(radius)
# cv2.circle(gray, center, radius, (255, 0, 0), 2)

x, y, w, h = cv2.boundingRect(cnt)
cv2.rectangle(onlyCircle, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("rectangle", onlyCircle)
key = cv2.waitKey(0)


rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)

angleRect = onlyCircle.copy()

cv2.drawContours(angleRect, [box], 0, (0, 0, 255), 2)


cv2.imshow("rectangleBetter", angleRect)
key = cv2.waitKey(0)


M = cv2.moments(cnt)
cx = int(M["m10"] / M["m00"])
cy = int(M["m01"] / M["m00"])
cv2.circle(onlyCircle, (cx, cy), 30, (0, 255, 0), 2)

cv2.imshow("MassCenter", onlyCircle)
key = cv2.waitKey(0)

(x, y), radius = cv2.minEnclosingCircle(cnt)
center = (int(x), int(y))
radius = int(radius)
cv2.circle(gray, center, radius, (0, 255, 0), 2)


min_circle = hough_circle.copy()

cv2.circle(min_circle, center, radius, (0, 255, 0), 2)

cv2.imshow("MIN_CIRCLE", min_circle)
key = cv2.waitKey(0)

# cv2.destroyAllWindows()
# Convert to grayscale.
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

output = hough_circle.copy()
# gray = cv2.cvtColor(onlyCircle, cv2.COLOR_BGR2GRAY)

# gray_blurred = cv2.blur(gray, (3, 3))
# detect circles in the image
img = cv2.medianBlur(hough_circle, 5)

cv2.imshow("Hough_circle", img)
key = cv2.waitKey(0)

cv2.imshow("Only_circle", onlyCircle)
key = cv2.waitKey(0)

gray_hough = cv2.cvtColor(onlyCircle, cv2.COLOR_BGR2GRAY)

cv2.imshow("Hough_circle_gray", gray_hough)
key = cv2.waitKey(0)

circles = cv2.HoughCircles(
    gray_hough,
    cv2.HOUGH_GRADIENT,
    1,
    20,
    param1=100,
    param2=30,
    minRadius=0,
    maxRadius=0,
)
# ensure at least some circles were found
print("Circle")
if circles is not None:
    print("found")
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    # show the output image
    cv2.imshow("output", np.hstack([onlyCircle, output]))
    cv2.waitKey(0)
