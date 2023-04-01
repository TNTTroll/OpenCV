# ---------- Imports
import cv2
import mediapipe as mp
import numpy as np
import time
from os import walk

import Fingers as F
import Inputs as I


# ---------- Variables
# <--- Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

onePose = True

# <--- Camera
cameraName = "Camera"

cam_Width = 640
cam_Height = 480

# <--- Color
black = (0, 0, 0)
white = (255, 255, 255)

# <--- Image
images = []
for (dirpath, dirnames, filenames) in walk("Images"):
    images.extend(filenames)
    break

images.sort()

screenImages = []
places = []

# <--- Pulse
ballPos = [cam_Width//2, cam_Height//2]
pulse = 1
radius = 10
grow = True

chooseGo = True
chooseTime = 3
choosePulse = 0

# <--- Game
inGame = False
start = stop = True
firstFrame = True
firstRound = True

needToGuess = "None" 
objection = [[0, 0], [10, 10]]

score = 0


# ---------- Settings
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)


# ---------- Defs
# <--- Texting
# Place a text on the screen
def printText(text, position, side):
	text = str(text)
	textSize = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 1, 2)

	if (side == "Top"):
		cv2.rectangle(frame, (0, 0), 
							 (cam_Width, 70), black, -1)
		cv2.putText(frame, text, (position[0]-(textSize[0][0]//2), position[1]), 
					cv2.FONT_HERSHEY_COMPLEX, .7, white, 2)

	elif (side == "Down"):
		cv2.rectangle(frame, (0, cam_Height), 
							 (cam_Width, cam_Height-70), black, -1)
		cv2.putText(frame, text, (position[0]-(textSize[0][0]//2), position[1]), 
					cv2.FONT_HERSHEY_COMPLEX, .7, white, 2)

# Draw a black block for the flags
def drawBlock():
	cv2.rectangle(frame, (0, cam_Height), 
				(cam_Width, cam_Height-110), black, -1)


# <--- Gaming
# Check if the game is Starting/Overing/In progress
def gameInProgress():
	global inGame, firstRound

	if (firstRound): startScreen()

	if (inGame):
		drawBlock()
		showMainImage()
	else:
		overScreen()

# Screen with a "Touch to play" and Play button
def startScreen():
	global pulse, grow

	if (grow):
		pulse += 1
	else:
		pulse -= 1

	if (pulse >= 40 or pulse <= 0):
		grow = not grow

	cv2.circle(frame, ballPos, radius+2+(pulse//2), black, -1)
	cv2.circle(frame, ballPos, radius+(pulse//2), white, -1)

	position = (int(cam_Width//2), int(cam_Height*.1))
	printText ( "Touch to Start" , position, "Top" )

# Screen that shows score and Play button
def overScreen():
	global ballPos, stop, start, firstRound, places

	if (not firstRound):
		if (stop):
			I.playAudio("Game Over")
			stop = False
			start = True
			places = []

		ballPos = [cam_Width//2, cam_Height//2]

		position = (int(cam_Width//2), int(cam_Height*.9))
		printText ( "Score: " + str(score) , position, "Down" )

	startScreen()


# <--- Imaging
# Show images on the screen every frame
def showMainImage():
	global screenImages

	for i in range(len(screenImages)):

		roi = frame[0:screenImages[i][0], 0:screenImages[i][1]]

		dst = cv2.add(cv2.bitwise_and(roi, roi, mask = screenImages[i][2]), 
					  screenImages[i][3])

		frame[0:screenImages[i][0], 0:screenImages[i][1]] = dst

# Refresh a flag list
def refreshFlags():
	global screenImages, places, firstFrame

	I.playAudio("Coin")

	firstFrame = True
	places = []
	screenImages = []


# <--- Choosing
# For global restart growing circle to right
def startPulsing(objection, land_pos):
	global choosePulse, images

	image = cv2.imread("Images/" + images[ images.index(objection[0]) ])
	resized = I.resizeImage(image, cam_Width, cam_Height)

	x1 = objection[1][0]
	y1 = objection[2][0]
	x2 = x1+resized.shape[1]
	y2 = y1+resized.shape[0]

	cv2.rectangle(frame, (x1, y1), (x2, y2), black, 3)

	sub_img = frame[y1:y2, x1:x2]
	white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
	res = cv2.addWeighted(sub_img, 0.5, white_rect, .5+choosePulse, 1.0)

	frame[y1:y2, x1:x2] = res

	choosePulse += .01
	choosePulse = round(choosePulse, 2)

# Choose a place after a certain amount of time 	
def choosePlace(objection, allPos):
	global choosePulse, needToGuess, inGame, score

	if (needToGuess == objection[0][0:objection[0].rfind(".")]):
		picked[3] = True
		score += 1

		refreshFlags()

	else: inGame = False

	choosePulse = 0


# ---------- Main
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
			needToGuess = I.openMainImage(frame, images, places, screenImages, cam_Width, cam_Height)
			firstFrame = False

		printText(needToGuess, [cam_Width//2, 40], "Top")


		# <--- Game
		gameInProgress()


		# <--- Poses
		if (isHand): 
			pose = F.poseFingers(land_pos)

			if (pose == "Pick"):

				if (start):
					if ( F.wasCaught(land_pos[8], ballPos, radius+(pulse//2)) ):
						firstRound = False    # Check if this is a first round in game or not
						start = False         # Disable start screen
						stop = True           # Allow to play Game Over audio
						inGame = True         # Set the game InProgress
						
						score = 0             # Reset score

				picked = I.getImage(places, land_pos)

				if (picked == "None"):
					choosePulse = 0
					timeSave = int(time.time())

				if (picked != "None" and not picked[3]):
					if (chooseGo):
						chooseGo = False
						timeSave = int(time.time())
					
					if (int(time.time()) - timeSave >= chooseTime):
						choosePlace(picked, land_pos)
						timeSave = int(time.time())

					else:
						startPulsing(picked, land_pos)

			elif (pose == "Skip" and onePose):
				refreshFlags()
				onePose = False

			elif (pose == "None"):
				onePose = True


		# <--- Show
		cv2.imshow(cameraName, frame)
		

		# <--- Close
		if cv2.waitKey(5) & 0xFF == 27: break


# ---------- Exit
camera.release()
cv2.destroyAllWindows()
cv2.waitKey(10)