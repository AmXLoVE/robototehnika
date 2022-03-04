import cv2
import math

img = cv2.imread("../../Resources/map.png")
mapRatio = 2.05

pathDrawing = True
path = []
pathLength = 0


def onMouse(event, x, y, flags, param):
    global path

    if event == cv2.EVENT_LBUTTONUP:
        if pathDrawing:
            path.append((x, y))


def distance(a, b):
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))


cv2.imshow("Map", img)
cv2.setMouseCallback("Map", onMouse)


while True:
    img = cv2.imread("../../Resources/map.png")

    if pathLength > 0:
        cv2.putText(img, f"{pathLength} meters.", (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    if path:
        for i in range(0, len(path) - 1):
            cv2.line(img, path[i], path[i+1], (255, 0, 0), 2)

    cv2.imshow("Map", img)

    if cv2.waitKey(1) & 0xFF == 32:
        if pathDrawing:
            pathDrawing = False
            for i in range(0, len(path) - 1):
                pathLength += distance(path[i], path[i+1])

            pathLength *= mapRatio
            pathLength = int(pathLength)
            cv2.putText(img, f"{pathLength} meters.", (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("Map", img)
            break

cv2.waitKey()
cv2.destroyAllWindows()