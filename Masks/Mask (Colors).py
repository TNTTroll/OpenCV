# ------------ Imports
import cv2
import numpy as np


# ------------ Variables
cam_Width = 320
cam_Height = 240

cameraName = "Camera"

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)

cv2.namedWindow(cameraName)

one = True
# ------------ Camera
while True:
	ret, frame = cam.read()

	red = frame.copy()
	red[:, :, 0] = 0
	red[:, :, 1] = 0

	invert = frame.copy()
	invert = 255 - invert

	blue = frame.copy()
	blue[:, :, 1] = 0
	blue[:, :, 2] = 0

	green = frame.copy()
	green[:, :, 0] = 0
	green[:, :, 2] = 0


	showOff = np.vstack(( np.hstack((red, invert)), np.hstack((blue, green)) ))

	cv2.imshow(cameraName, showOff)

	k = cv2.waitKey(10) & 0xFF

	if ((not ret) or (k == ord('q') or k == ord('й'))):
		break


# ------------ Exit
cam.release()
cv2.destroyAllWindows()
cv2.waitKey(10)