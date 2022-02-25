import cv2

gridWidth = 3
gridHeight = 3

img = cv2.imread("../Resources/cat.jpg")
height, width = img.shape[:2]

frameWidth = width / gridWidth
frameHeight = height / gridHeight

cv2.imshow("Image", img)
cv2.waitKey()
cv2.destroyAllWindows()

for x in range(0, gridWidth):
    for y in range(0, gridHeight):
        frame = img[int(frameHeight * y) : int(frameHeight * (y + 1)), int(frameWidth * x) : int(frameWidth * (x + 1))]
        cv2.imshow(f"{x}, {y}", frame)
        cv2.imwrite(f"Results/{y} {x}.jpg", frame)

cv2.waitKey()