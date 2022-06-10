import numpy as np
import cv2

cv2.namedWindow("Output AR")

# Ввод картинок
capture = cv2.VideoCapture("Input/video_2022-06-10_04-14-49.mp4")
success, image = capture.read()
(imgH, imgW) = image.shape[:2]

source = cv2.imread("Input/DxyWAcDWkAE9JFD.jpg")

while success:
	success, image = capture.read()

	# Находим маркеры
	arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
	arucoParams = cv2.aruco.DetectorParameters_create()
	(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
		parameters=arucoParams)

	if len(corners) != 4:
		print(len(corners))
		image = cv2.resize(image, None, fx=0.8, fy=0.8)
		cv2.imshow("Output AR", image)
		cv2.waitKey()
		continue

	# Определяем маркеры
	# ids = ids.flatten()
	#
	# for (markerCorner, markerID) in zip(corners, ids):
	#     corners = markerCorner.reshape((4, 2))
	#     (topLeft, topRight, bottomRight, bottomLeft) = corners
	#     topRight = (int(topRight[0]), int(topRight[1]))
	#     bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
	#     bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
	#     topLeft = (int(topLeft[0]), int(topLeft[1]))
	#
	#     cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
	#     cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
	#     cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
	#     cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
	#
	#     cX = int((topLeft[0] + bottomRight[0]) / 2.0)
	#     cY = int((topLeft[1] + bottomRight[1]) / 2.0)
	#     cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
	#     # draw the ArUco marker ID on the image
	#     cv2.putText(image, str(markerID),
	#         (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
	#         0.5, (0, 255, 0), 2)
	#     print("[INFO] ArUco marker ID: {}".format(markerID))
	#     # show the output image
	#
	# cv2.imshow("Image", image)
	# cv2.waitKey()

	ids = ids.flatten()
	refPts = []

	# Последовательность углов
	for i in (0, 1, 3, 2):
		j = np.squeeze(np.where(ids == i))
		corner = np.squeeze(corners[j])
		refPts.append(corner)

	# Указываем координаты углов лев верх, прав верх, прав ниж, лев ниж
	(refPtTL, refPtTR, refPtBR, refPtBL) = refPts
	dstMat = [refPtTL[0], refPtTR[1], refPtBR[2], refPtBL[3]]
	dstMat = np.array(dstMat)

	#Координаты углов соурса
	(srcH, srcW) = source.shape[:2]
	srcMat = np.array([[0, 0], [srcW, 0], [srcW, srcH], [0, srcH]])

	# Ищем гомографию, изменяем перспективу
	(H, _) = cv2.findHomography(srcMat, dstMat)
	warped = cv2.warpPerspective(source, H, (imgW, imgH))

	# Создаем маску - черную область за пределами соурса
	mask = np.zeros((imgH, imgW), dtype="uint8")
	cv2.fillConvexPoly(mask, dstMat.astype("int32"), (255, 255, 255),
		cv2.LINE_AA)

	# Красивая обводка соурса
	rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	mask = cv2.dilate(mask, rect, iterations=2)

	maskScaled = mask.copy() / 255.0
	maskScaled = np.dstack([maskScaled] * 3)

	# Копируем соурс на image
	warpedMultiplied = cv2.multiply(warped.astype("float"), maskScaled)
	imageMultiplied = cv2.multiply(image.astype(float), 1.0 - maskScaled)
	output = cv2.add(warpedMultiplied, imageMultiplied)
	output = output.astype("uint8")
	output = cv2.resize(output, None, fx=0.8, fy=0.8)

	cv2.imshow("Output AR", output)
	cv2.waitKey()

cv2.waitKey()