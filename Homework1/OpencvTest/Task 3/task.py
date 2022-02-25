import cv2
import time

video = cv2.VideoCapture(0)
videoSize = int(video.get(3)), int(video.get(4))
saveVideo = cv2.VideoWriter("Results/video.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, videoSize)

while video.isOpened():
    _, img = video.read()

    saveVideo.write(img)

    cv2.imshow("Camera", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('s'):
        cv2.imwrite(f"Results/Image {time.time()}.jpg", img)

video.release()
saveVideo.release()

cv2.destroyAllWindows()