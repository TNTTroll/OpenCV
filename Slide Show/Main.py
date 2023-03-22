# ---------- Imports
import cv2
import mediapipe as mp
import numpy as np
from os import walk

import Fingers as F


# ---------- Variables
# <--- Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# <--- Camera
cameraName = "Camera"

cam_Width = 640
cam_Height = 480

# <--- Images
images = []
for (dirpath, dirnames, filenames) in walk("Images"):
    images.extend(filenames)
    break

inUse = None

accurency = 50


# <--- Commands
stop = True

count = 0
step = 1


# ---------- Settings
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)


# ---------- Defs
# Def for show an image on the screen
# Get palm's position and place an image between three bases of: palm, pinky and index
def showImage():
	global inUse

	scale_percent = F.size(land_pos)

	if (type(inUse).__name__ == "NoneType"):
		inUse = openImage(images)

	resized = resizeImage(inUse, land_pos)

	x = (land_pos[0][0] + land_pos[5][0] + land_pos[17][0]) // 3 
	y = (land_pos[0][1] + land_pos[5][1] + land_pos[17][1]) // 3

	move = np.float32([ [1, 0, x - (resized.shape[1] // 2)],
                        [0, 1, y - (resized.shape[0] // 2)],
                        [0, 0, 1] ])

	adding = cv2.warpPerspective(resized, move, (cam_Width, cam_Height))

	rows,cols,channels = adding.shape
	roi = frame[0:rows, 0:cols]

	img2gray = cv2.cvtColor(adding, cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)

	img1_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
	img2_fg = cv2.bitwise_and(adding, adding, mask = mask)

	dst = cv2.add(img1_bg,img2_fg)
	frame[0:rows, 0:cols ] = dst


# Def for open an image from folder on PC
# If folder is empty the image will be "Empty.png"  
def openImage(images, way):
	global count

	if ( count >= len(images) ):
		count = 0

	image = None
	if ( len(images) > 0 ):
		image = cv2.imread("Images/" + images[count])

	else:
		image = cv2.imread("Empty.png")

	while (type(image).__name__ == "NoneType"):	
		if (way == "Forth"):
			count += 1
			image = openImage(images, "Forth")
		else:
			count -= 1
			image = openImage(images, "Back")

	return image


# Def for resize an image according to palm's size
# Also size can be changed with Index (+) and Middle (-) fingers
def resizeImage(image, allPos):
	global step

	imWidth = inUse.shape[1]
	imHeight = inUse.shape[0]

	maximumSize = getAverage(F.size(allPos) * 10)
	imageSize = max(imHeight, imWidth)

	height = width = maximumSize
	if (imageSize == imHeight):
		height = maximumSize
		width = int(maximumSize * imWidth / imHeight)
	else:
		height = int(maximumSize * imHeight / imWidth)
		width = maximumSize


	width = int(width * step)
	height = int(height * step)


	width = max(1, width)
	height = max(1, height)

	if ( width == 1 or height == 1 ):
		step += .1

	width = min(width, cam_Width)
	height = min(height, cam_Height)

	if ( width == cam_Width or height == cam_Height ):
		step -= .1


	step = round(step, 2)
	resized = cv2.resize(inUse, (width, height), interpolation = cv2.INTER_AREA)

	return resized


# Def for average maximum size
# That is for prevent an image from giggling
averArr = []
averStep = 0
def getAverage(size):
	global averStep, averArr

	if (len(averArr) < accurency):
		averArr.append(size)

	else:
		averStep += 1
		if (averStep >= accurency):
			averStep = 0

		averArr[averStep] = size

	averSize = int( sum(averArr) / len(averArr) )

	return averSize


# ---------- Main
inUse = openImage(images, "Forth")

with mp_hands.Hands(min_detection_confidence=0.5,
    				min_tracking_confidence=0.5) as hands:

	while camera.isOpened():
		ret, frame = camera.read()
		if not ret: continue


		# <--- Frame
		frame = cv2.flip(frame, 1)

		lands = frame.copy()
		lands = cv2.cvtColor(lands, cv2.COLOR_BGR2RGB)
		results = hands.process(lands)


		isHand = False
		
		# <--- Hands
		land_pos = []

		lands = cv2.cvtColor(lands, cv2.COLOR_RGB2BGR)
		if results.multi_hand_landmarks:

			isHand = True

			for hand_landmarks in results.multi_hand_landmarks:
				mp_drawing.draw_landmarks(
            			lands, 
            			hand_landmarks, 
            			mp_hands.HAND_CONNECTIONS
            		)

			for id, landmark in enumerate(hand_landmarks.landmark):
				h, w, c = lands.shape
				land_pos.append([int(landmark.x*w), int(landmark.y*h)])


		# <--- Command
		if (isHand):

			pose = F.poseFingers(land_pos)

			if (pose == "Default"):
				stop = True

			elif (pose == "Forward"):
				if (stop):
					stop = False
					count += 1

					inUse = openImage(images, "Forth")

			elif (pose == "Backward"):
				if (stop):
					stop = False
					count -= 1

					if (count <= -1):
						count = len(images) - 2

					inUse = openImage(images, "Back")

			elif (pose == "Zoom in"):
				if (stop):
					stop = False

					step += .1
					step = round(step, 2)

			elif (pose == "Zoom out"):
				if (stop):
					stop = False
					
					step -= .1
					step = round(step, 2)
			

			if (pose != "Close"):
				showImage()


		# <--- Show
		cv2.imshow(cameraName, frame)
		

		# <--- Close
		if cv2.waitKey(5) & 0xFF == 27: break


# ---------- Exit
camera.release()
cv2.destroyAllWindows()
cv2.waitKey(10)