# ------------ Imports
import cv2
import numpy as np
from math import sin, cos, pi


# ------------ Variables
cam_Width = 640
cam_Height = 480
offSet = 20
speed = 1
tick = 0 

cameraName = "Camera"

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)

cv2.namedWindow(cameraName)


# ------------ Camera
while True:
	ret, frame = cam.read()

	tick += speed/10
	if (tick >= pi*2):
		tick = 0

	move = np.float32([ [1, 0, offSet * sin(tick)],
                        [0, 1, offSet * cos(tick)],
                        [0, 0, 1] ])
	

	ghost = cv2.warpPerspective(frame, move, (cam_Width, cam_Height))


	show = cv2.addWeighted(frame, 0.8, ghost, 0.2, 0.0)
	cv2.imshow(cameraName, show)


	k = cv2.waitKey(10) & 0xFF

	if ((not ret) or (k == ord('q') or k == ord('й'))):
		break


# ------------ Exit
cam.release()
cv2.destroyAllWindows()
cv2.waitKey(10)