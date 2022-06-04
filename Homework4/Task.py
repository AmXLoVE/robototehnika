import random
import cv2


def add_noise(image, percent):
    row, col = image.shape
    number_of_pixels = int(row * col * percent / 100)
    for i in range(number_of_pixels):
        y_coord = random.randint(0, row - 1)
        x_coord = random.randint(0, col - 1)
        image[y_coord][x_coord] = 255
    number_of_pixels = int(col * row * percent / 100)
    for i in range(number_of_pixels):
        y_coord = random.randint(0, row - 1)
        x_coord = random.randint(0, col - 1)
        image[y_coord][x_coord] = 0
    return image


def OnPercentChange(value):
    global noise_percent, img
    noise_percent = value
    img = add_noise(cv2.imread("OriginalImage/DxyWAcDWkAE9JFD.jpg",
                 cv2.IMREAD_GRAYSCALE), noise_percent)
    cv2.imshow("Noise", img)
    cv2.imshow("Averaging", cv2.blur(img, ksize=(9, 9)))
    cv2.imshow("Median", cv2.medianBlur(img, ksize=9))
    cv2.imshow("GaussianBlur", cv2.GaussianBlur(img, ksize=(9, 9), sigmaX=15, sigmaY=15))
    cv2.imshow("BilateralFiltering", cv2.bilateralFilter(img, d=9, sigmaColor=150, sigmaSpace=150))


img = cv2.imread("OriginalImage/DxyWAcDWkAE9JFD.jpg",
                 cv2.IMREAD_GRAYSCALE)
noise_percent = 0
cv2.namedWindow("Noise")
cv2.namedWindow("Averaging")
cv2.namedWindow("Median")
cv2.namedWindow("GaussianBlur")
cv2.namedWindow("BilateralFiltering")
cv2.createTrackbar("Noise percent", "Noise", 0, 100, OnPercentChange)
cv2.imshow("Noise", img)
cv2.waitKey()
cv2.destroyAllWindows()
