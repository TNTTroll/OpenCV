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


# ------------ Camera
while True:
	ret, thresh = cam.read()


	thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

	_, frame = cv2.threshold(thresh,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	

	skel = np.zeros(frame.shape, np.uint8)

	element = cv2.getStructuringElement(cv2.MORPH_CROSS, (10,10))
	open2 = cv2.morphologyEx(frame, cv2.MORPH_OPEN, element)
	temp = cv2.subtract(frame, open2)
	skel = cv2.bitwise_or(skel,temp)
	
	kernel = np.array([[1, 1, 1],
  					   [1, 10, 1],
                       [1, 1, 1]])

	sharp_filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

	sobelxy = cv2.Sobel(frame, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=1)

	cv2.imshow(cameraName, sobelxy)

	k = cv2.waitKey(10) & 0xFF

	if ((not ret) or (k == ord('q'))):
		break


# ------------ Exit
cam.release()
cv2.destroyAllWindows()
cv2.waitKey(10)