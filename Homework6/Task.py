import cv2
from matplotlib import pyplot as plt

img = cv2.imread("Input/DxyWAcDWkAE9JFD.jpg")
edges = cv2.Canny(img, 100, 200)

cv2.imshow("img", edges)
cv2.waitKey()