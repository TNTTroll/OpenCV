# ------------ Imports
import cv2
import numpy as np


# ------------ Variables
cam_Width = 320
cam_Height = 240

B_Min, B_Max = 0, 255
G_Min, G_Max = 0, 255
R_Min, R_Max = 0, 255

posX, posY = 0, 0
step = 50
touched = False


cameraName = "Camera"

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)

cv2.namedWindow(cameraName)


# ------------ Functions
def onMouse(event, x, y, flags, param):
	global posX, posY
	global touched
	if event == cv2.EVENT_LBUTTONDOWN:
		posX = y
		posY = x

		touched = True


# ------------ Settings
cv2.setMouseCallback(cameraName, onMouse)

colors = [np.zeros((40, 320, 3), np.uint8),
		  np.zeros((40, 320, 3), np.uint8)]


# ------------ Camera
while True:
	ret, frame = cam.read()

	if touched:
		try:
			pick_color = frame[posX, posY]
		except IndexError:
			pick_color = frame[cam_Height-1, cam_Width-1]

		B_Min = max(0, int(pick_color[0]) - step)
		G_Min = max(0, int(pick_color[1]) - step)
		R_Min = max(0, int(pick_color[2]) - step)

		colors[0][:] = (B_Min, G_Min, R_Min)


		B_Max = min(255, int(pick_color[0]) + step)
		G_Max = min(255, int(pick_color[1]) + step)
		R_Max = min(255, int(pick_color[2]) + step)
		
		colors[1][:] = (B_Max, G_Max, R_Max)

		touched = False

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(frame, (B_Min, G_Min, R_Min), (B_Max, G_Max, R_Max))
	opened = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel = np.ones((3, 3)))

	execution = cv2.bitwise_and(frame,frame,mask=opened)

	videos_part = np.hstack((frame, execution))
	colors_part = np.hstack((colors[0], colors[1])) 

	showOff = np.vstack((videos_part, colors_part))

	cv2.imshow(cameraName, showOff)


	k = cv2.waitKey(10) & 0xFF

	if ((not ret) or (k == ord('q') or k == ord('й'))):
		break


# ------------ Exit
cam.release()
cv2.destroyAllWindows()
cv2.waitKey(10)