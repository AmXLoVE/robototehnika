import math
import numpy as np
import cv2

image = np.zeros((510, 510, 3), np.uint8)
mousePosition = (0, 0)
value = 255
imgHSV = None
Ox = 0
Oy = 0
diagram = cv2.namedWindow("Diagram")

#distance between two dots
def GetDistance():
    return int(math.sqrt((0 - Ox) * (0 - Ox) + (0 - Oy) * (0 - Oy)))


# HSV diagram
def GetHSVDiagram():
    global Ox, Oy
    for i in range(510):
        for j in range(510):
            Ox = i - 255
            Oy = j - 255

            atan = math.atan2(Oy, Ox)
            if atan < 0:
                atan += 2 * math.pi
            atan *= 180 / (2 * math.pi)

            distance = GetDistance()
            v = value
            if distance > 255:
                v = 0
            image[i, j] = (atan, distance, v)
    return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

#Get value from trackbar
def GetValue(args):
    global value, imgHSV
    value = args
    imgHSV = GetHSVDiagram()
    cv2.imshow("Diagram", imgHSV)
    cv2.waitKey(100)

#get color, set rgb, ycrcb, lab
def mouseClick(event, x, y, flags, param):
    global mousePosition, imgHSV
    if event == cv2.EVENT_LBUTTONDOWN:
        mousePosition = (x, y)
        color = imgHSV[mousePosition]
        colorRamp = np.ones((150, 200, 3), np.uint8)
        for i in range(150):
            for j in range(200):
                colorRamp[i, j] = color
        cv2.namedWindow("RGB", cv2.WINDOW_NORMAL)
        cv2.namedWindow("YCrCB", cv2.WINDOW_NORMAL)
        cv2.namedWindow("LAB", cv2.WINDOW_NORMAL)
        ycrcb = cv2.cvtColor(colorRamp, cv2.COLOR_BGR2YCrCb)
        rgb = cv2.cvtColor(colorRamp, cv2.COLOR_BGR2RGB)
        lab = cv2.cvtColor(colorRamp, cv2.COLOR_BGR2LAB)
        cv2.imshow("RGB", rgb)
        cv2.imshow("YCrCB", ycrcb)
        cv2.imshow("LAB", lab)


imgHSV = GetHSVDiagram()
cv2.imshow("Diagram", imgHSV)
cv2.setMouseCallback("Diagram", mouseClick)
cv2.createTrackbar("Value", "Diagram", value, 255, GetValue)
cv2.waitKey()
