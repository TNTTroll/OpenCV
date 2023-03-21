# ------------ Imports
import cv2
import numpy as np


# ------------ Variables
cam_Width = 640
cam_Height = 480

cameraName = "Camera"

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)

cv2.namedWindow(cameraName)


backSub = cv2.createBackgroundSubtractorKNN()


# ------------ Camera
while True:
	_, frame = cam.read()


	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 0)

	fgMask = backSub.apply(blurred)
	execution = cv2.bitwise_and(blurred,blurred,mask=fgMask)
	
	
	threshold = cv2.threshold(execution, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] 

	cv2.imshow(cameraName, threshold)

	k = cv2.waitKey(10) & 0xFF
	if ((not _) or (k == ord('q'))):
		break


# ------------ Exit
cam.release()
cv2.destroyAllWindows()
cv2.waitKey(10)