import cv2
import math
import numpy as np

img = cv2.imread("../../Resources/road.jpg")
imgSize = (img.shape[1], img.shape[0])
out_image = None
points = []


def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if len(points) < 3:
            points.append((x, y))


def distance(a, b):
    return int(math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])))


cv2.imshow("Image", img)
cv2.setMouseCallback("Image", onMouse)

while True:
    img = cv2.imread("../../Resources/road.jpg")

    if len(points) == 3:
        width = distance(points[0], points[1])
        height = distance(points[1], points[2])

        fromMatrix = np.float32([points[0], points[1], points[2]])
        toMatrix = np.float32([
            [imgSize[0] / 2 - width / 2, imgSize[1] / 2 - height / 2],
            [imgSize[0] / 2 + width / 2, imgSize[1] / 2 - height / 2],
            [imgSize[0] / 2 + width / 2, imgSize[1] / 2 + height / 2]
        ])
        affineMatrix = cv2.getAffineTransform(fromMatrix, toMatrix)

        topView = cv2.warpAffine(img, affineMatrix, imgSize)
        cv2.imshow(f"Crossroad top view", topView)

    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), -1)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()