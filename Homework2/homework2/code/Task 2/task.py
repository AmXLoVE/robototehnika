import cv2

cap = cv2.VideoCapture("../../Resources/video.mp4")
frame_size = int(cap.get(3)), int(cap.get(4))
saveVideo = cv2.VideoWriter("Result/saved_video.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 60, frame_size)

annotations = [(1, 200, "Text 11111111111111122222222222222222222222"), (200, 500, "Text 221212121212121212121212"), (500, 1000, "Робототехника лучший предмет")]
currentAnnotation = None

while cap.isOpened():
    success, frame = cap.read()
    frameIndex = cap.get(1)

    if not success:
        break

    for annotation in annotations:
        if annotation[1] == frameIndex:
            currentAnnotation = None
        if annotation[0] == frameIndex:
            currentAnnotation = annotation

    if currentAnnotation:
        cv2.putText(frame, currentAnnotation[2], (1000, 1000), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

    print("please, wait...")
    saveVideo.write(frame)

print("done")
cap.release()
saveVideo.release()
cv2.destroyAllWindows()