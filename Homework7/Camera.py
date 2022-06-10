import cv2

cv2.namedWindow("look", 1)
# Включите ip камеру
video = 'https://192.168.0.105:8080/'  # http: // admin: admin @     Address /
capture = cv2.VideoCapture(video)

num = 0
while True:
    success, img = capture.read()
    cv2.imshow("look", img)
    c= cv2.waitKey(100)
    if c== 27:
        # esc ключ для выхода
        print("esc break...")
        break
    if c== ord(' '):
        # Пробел для сохранения изображения
        num = num + 1
        filename = "picture_%s.jpg" % num
        cv2.imwrite(filename, img)

capture.release()
cv2.destroyWindow("look")