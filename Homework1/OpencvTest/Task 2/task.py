import math
import cv2
import numpy as np


img = cv2.imread("../Resources/cat.jpg")
out_image = None
points = []

mousePressed = False
selectedPointIndex = -1

def onMouse(event, x, y, flags, param):
    global mousePressed, selectedPointIndex
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, point in enumerate(points):
            if distance(point, (x, y)) < 20:
                selectedPointIndex = i
        mousePressed = True

    if event == cv2.EVENT_LBUTTONUP:
        selectedPointIndex = -1
        mousePressed = False

    if event == cv2.EVENT_MOUSEMOVE:
        if mousePressed and selectedPointIndex != -1:
            points[selectedPointIndex] = (x, y)

    if event == cv2.EVENT_LBUTTONDBLCLK:
        points.append((x, y))
        pass

cv2.imshow("Image", img)
cv2.setMouseCallback("Image", onMouse)

def distance(a, b):
    return int(math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])))

while True:
    img = cv2.imread("../Resources/cat.jpg")

    if len(points) == 4:
        warpedWidth = distance(points[0], points[1])
        warpedHeight = distance(points[0], points[3])

        fromMatrix = np.float32([points[0], points[1], points[2], points[3]])
        toMatrix = np.float32([
            [0, 0],
            [warpedWidth, 0],
            [warpedWidth, warpedHeight],
            [0, warpedHeight]
        ])
        matrix = cv2.getPerspectiveTransform(fromMatrix, toMatrix)
        out_image = cv2.warpPerspective(img, matrix, (warpedWidth, warpedHeight))
        cv2.imshow("Warped image", out_image)

        cv2.line(img, points[0], points[1], (255, 0, 0), 2)
        cv2.line(img, points[1], points[2], (255, 0, 0), 2)
        cv2.line(img, points[2], points[3], (255, 0, 0), 2)
        cv2.line(img, points[3], points[0], (255, 0, 0), 2)

    for i, point in enumerate(points):
        cv2.circle(img, point, 5, (0, 0, 255), -1)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()