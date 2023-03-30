# ---------- Imports
import cv2
import mediapipe as mp
import numpy as np
import time
from os import walk
from random import randint 

import Fingers as F
import Images as I


# ---------- Variables
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cameraName = "Camera"

cam_Width = 640
cam_Height = 480

images = []
for (dirpath, dirnames, filenames) in walk("Images"):
    images.extend(filenames)
    break

images.sort()

screenImages = []

guessed = []
pic = "None"

places = []
firstFrame = True

chooseGo = True
chooseTime = 3
choosePulse = 0

objection = [[0, 0], [10, 10]]


# ---------- Settings
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)


# ---------- Defs
def printText(text, position):
	text = str(text)

	size = 4
	cv2.rectangle(frame, (position[0]-size, position[1]-size*2), 
						 (position[0]+size*5, position[1]+size), (0, 0, 0), -1)
	cv2.putText(frame, text, (position[0], position[1]), 
				cv2.FONT_HERSHEY_COMPLEX, .7, (255, 255, 255), 2)


def guessPic(images):

	i = randint(0, len(images)-1)
	while (i in guessed):
		i = randint(0, len(images)-1)

	return images[i]


def showMainImage():
	global screenImages, guessed

	for i in range(len(screenImages)):

		if i in guessed: continue

		roi = frame[0:screenImages[i][0], 0:screenImages[i][1]]

		dst = cv2.add(cv2.bitwise_and(roi, roi, mask = screenImages[i][2]), 
					  screenImages[i][3])

		frame[0:screenImages[i][0], 0:screenImages[i][1]] = dst


def choosePlace(objection, allPos):

	global choosePulse, images
	global pic, guessed

	if (pic == objection[0]):
		guessed.append( images.index(pic) )
		pic = guessPic(images)
		picked[3] = True


	choosePulse = 0

	return True


# For global restart growing circle to right
def startPulsing(objection, land_pos):
	global choosePulse, images

	image = cv2.imread("Images/" + images[ images.index(objection[0]) ])

	resized = I.resizeImage(image, cam_Width, cam_Height)

	x1 = objection[1][0]
	y1 = objection[2][0]
	x2 = x1+resized.shape[1]
	y2 = y1+resized.shape[0]


	cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

	sub_img = frame[y1:y2, x1:x2]
	white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255

	res = cv2.addWeighted(sub_img, 0.5, white_rect, .5+choosePulse, 1.0)

	frame[y1:y2, x1:x2] = res


	choosePulse += .01
	choosePulse = round(choosePulse, 2)


# ---------- Main
pic = guessPic(images)

with mp_hands.Hands(min_detection_confidence=0.5,
    				min_tracking_confidence=0.5) as hands:

	while camera.isOpened():
		ret, frame = camera.read()
		if not ret: continue


		# <--- Frame
		frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
		results = hands.process(frame)


		isHand = False
		
		# <--- Hands
		land_pos = []

		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
		if results.multi_hand_landmarks:

			isHand = True

			# Draw markers for first hand and save all of its coords
			for hand_landmarks in results.multi_hand_landmarks:
				mp_drawing.draw_landmarks(
            			frame, 
            			hand_landmarks, 
            			mp_hands.HAND_CONNECTIONS
            		)

			for id, landmark in enumerate(hand_landmarks.landmark):
				h, w, c = frame.shape
				land_pos.append([int(landmark.x*w), int(landmark.y*h)])

		if (firstFrame):
			I.openMainImage(frame, images, places, screenImages, cam_Width, cam_Height)
			firstFrame = False

		else:
			showMainImage()
			printText(pic, [cam_Width//2, 40])


		# <--- Poses
		if (isHand): 
			pose = F.poseFingers(land_pos)

			if (pose == "Pick"):

				picked = I.getImage(places, land_pos)

				if (picked != "None" and not picked[3]):
					if (chooseGo):
						chooseGo = False
						timeSave = int(time.time())
					
					if (int(time.time()) - timeSave >= chooseTime):
						choosePlace(picked, land_pos)

						timeSave = int(time.time())


					else:
						startPulsing(picked, land_pos)


		# <--- Show
		cv2.imshow(cameraName, frame)
		

		# <--- Close
		if cv2.waitKey(5) & 0xFF == 27: break


# ---------- Exit
camera.release()
cv2.destroyAllWindows()
cv2.waitKey(10)