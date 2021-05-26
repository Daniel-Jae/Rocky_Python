# from typing_extensions import ParamSpecArgs
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("Processing/test_image.jpeg", 1)
img = cv2.resize(img, (0, 0), fx=0.7, fy=0.7)

# width = int(img.get(3))
# heigth = int(img.get(4))

# function to display the coordinates of
# of the points clicked on the image

W = 400
pts1 = np.float32()
test = np.array([1, 1])


def my_filled_circle(img, center):
    thickness = -1
    line_type = 8
    cv2.circle(img, center, W // 32, (0, 0, 255), thickness, line_type)


def click_event(event, x, y, flags, params):

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

        pt = np.float32([x, y])
        print(pt)
        print(np.append(test, pt))

        print(test)
        test2 = test

        pts2 = test
        pts1 = np.append(pts2, pt)
        print(pts1)
        # np.append(ptHuman, pt)
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, "Roboter", (x + 10, y + 10), font, 0.9, (0, 0, 255), 2)
        cv2.circle(img, (x, y), 10, (0, 0, 255), 2)
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
        cv2.imshow("image", img)

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, "Mensch", (x + 10, y + 10), font, 0.9, (255, 0, 0), 2)
        # cv2.putText(img, str(x) + "," + str(y), (x, y), font, 1, (255, 255, 0), 2)
        cv2.circle(img, (x, y), 10, (255, 0, 0), 2)
        cv2.circle(img, (x, y), 2, (255, 0, 0), -1)
        cv2.imshow("image", img)


ptHuman = np.float32()
ptRobot = np.float32()


cv2.imshow("image", img)
cv2.setMouseCallback("image", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(ptHuman)
print(pts1)
pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])

M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (300, 300))
plt.subplot(121), plt.imshow(img), plt.title("Input")
plt.subplot(122), plt.imshow(dst), plt.title("Output")
plt.show()

pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])


print(pts1)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_black = np.array([0, 0, 0])
upper_black = np.array([213, 40, 55])

mask = cv2.inRange(hsv, lower_black, upper_black)

result = cv2.bitwise_and(img, img, mask=mask)

# cv2.imshow("Image", img)
cv2.imshow("Image", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
