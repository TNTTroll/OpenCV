# ---------- Imports
import cv2
import mediapipe as mp

import Fingers as F
import Logic as L


# ---------- Variables
# <--- Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# <--- Camera
cameraName = "Camera"

cam_Width = 640
cam_Height = 480

# <--- Colors
white = (255, 255, 255)
black = (0, 0, 0)

# <--- Ball
ballPos = [cam_Width//2, cam_Height//2]

radius = 10
gravity = 5

pulse = 1
grow = True

# <--- Labels
size = 20 
score = 0
start = stop = True
inGame = False

firstRound = True


# ---------- Settings
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)


# ---------- Defs
# Print a text on the screen
def printText(text, position, color, w):
	text = str(text)
	cv2.rectangle(frame, (position[0]-size//2, position[1]-size), 
						 (position[0]+size*w, position[1]+size//2), black, -1)
	cv2.putText(frame, text, (position[0], position[1]), 
				cv2.FONT_HERSHEY_COMPLEX, .7, color, 2)

# Draw a ball that fly down every frame
def drawFallCircle():
	global ballPos

	cv2.circle(frame, ballPos, radius+2, black, -1)
	cv2.circle(frame, ballPos, radius, white, -1)

	position = (int(cam_Width//2)-30, int(cam_Height*.9))
	printText ( score , position, white, 2 )

# Check if the game in progress
# If YES - draw falling balls
# IF NO - show score and Play button
def gameInProgress():
	global ballPos 
	global inGame, firstRound

	if (firstRound): startScreen()

	if ( L.ballOutOfLimits(ballPos, cam_Height) ): inGame = False


	if (inGame):
		drawFallCircle()
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

	position = (int(cam_Width//2)-90, int(cam_Height*.1))
	printText ( "Touch to Start" , position, white, 10 )

# Screen that shows score and Play button
def overScreen():
	global ballPos
	global stop, start, firstRound

	if (not firstRound):
		if (stop):
			L.playAudio("Game Over")
			stop = False
			start = True

		ballPos = [cam_Width//2, cam_Height//2]

		position = (int(cam_Width//2)-70, int(cam_Height*.9))
		printText ( "Game Over" , position, white, 7 )

		position = (int(cam_Width//2)-70, int(cam_Height*.8))
		printText ( "Score: " + str(score) , position, white, 7 )

	startScreen()


# ---------- Main
with mp_hands.Hands(min_detection_confidence=0.5,
    				min_tracking_confidence=0.5) as hands:

	while camera.isOpened():
		ret, frame = camera.read()
		if not ret: continue

		# Check if there are any hands
		first = False


		# <--- Frame
		frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
		results = hands.process(frame)


		# <--- Hands
		land_pos = []

		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
		if results.multi_hand_landmarks:

			first = True

			# Draw markers for first hand and save all of its coords
			for hand_landmarks in [results.multi_hand_landmarks[0]]:
				mp_drawing.draw_landmarks(
            			frame, 
            			hand_landmarks, 
            			mp_hands.HAND_CONNECTIONS
            		)

			for id, landmark in enumerate(hand_landmarks.landmark):
				h, w, c = frame.shape

				if (id == 8):
					land_pos.append([int(landmark.x*w), int(landmark.y*h)])

		# <--- Draw ball
		gameInProgress()

		if (not start):
			ballPos[1] += int(gravity)


		# <--- Catch
		if (first):
			if (start):
				if ( F.wasCaught(land_pos[0], ballPos, radius+(pulse//2)) ):
					firstRound = False    # Check if this is a first round in game or not
					start = False         # Disable start screen
					stop = True           # Allow to play Game Over audio
					inGame = True         # Set the game InProgress
					
					score = 0             # Reset score
					ballPos = L.spawnBall(ballPos, cam_Width, cam_Height)


			if ( F.wasCaught(land_pos[0], ballPos, radius) ):
				score += 1
				ballPos = L.spawnBall(ballPos, cam_Width, cam_Height)

				if (score % 5 == 0):
					gravity += 1


		# <--- Show
		cv2.imshow(cameraName, frame)
		

		# <--- Close
		if cv2.waitKey(5) & 0xFF == 27: break


# ---------- Exit
camera.release()
cv2.destroyAllWindows()
cv2.waitKey(10)