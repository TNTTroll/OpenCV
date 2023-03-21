# Program for English sign language. Use two hands
# Right is for language; Left is for commands
# Letters are created accroding to English sign language
# Commands are created on free way

# Thumb + Index = Update command
# Thumb + Index = Space
# Thumb = Erase
# Index = Point
# Middle = Comma
# Ring = Question mark
# Pinky = Explament mark 


# ---------- Imports
import cv2
import mediapipe as mp
import time 

import Fingers as F


# ---------- Variables
# <--- Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

# <--- Camera
cam_Width = 640
cam_Height = 480

cameraName = "Camera"

# <--- Colors
white = (255, 255, 255)
black = (0, 0, 0)

# <--- Label
size = 20

# <--- Text
string = ""
canWrite = True

stick = 0
animationSpeed = 6

restartGo = True
restartTime = 5
restartPulse = 1

add = True


# ---------- Settings
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)


# ---------- Defs
# Print text on the screen
# Check if the text size shorter than screen width
def printText(text, position, scale, left):
	global canWrite

	text = str(text)
	cv2.rectangle(frame, (position[0]-size, position[1]-size*2), 
						 (position[0]+size*scale, position[1]+size), black, -1)
	cv2.putText(frame, text, (position[0], position[1]), 
				cv2.FONT_HERSHEY_COMPLEX, 1, white, 2)

	if (len(text) > 0):
		if (text[-1] != "|"):
			text += "|"


	if (left):
		textSize = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 1, 2)

		if (textSize[0][0] < cam_Width - 20):
			canWrite = True
		else:
			canWrite = False


# For global restart growing circle to right
def startPulsing():
	global restartPulse

	position = (cam_Width//10*9, cam_Height//2)

	cv2.circle(frame, position, 48, black, -1)
	cv2.circle(frame, position, restartPulse*2, white, -1)
	
	restartPulse += 1


# Restart string 
def restartString():
	global string, restartGo

	restartGo = True
	string = ""


# ---------- Main
with mp_hands.Hands(min_detection_confidence=0.5,
    				min_tracking_confidence=0.5) as hands:

	while camera.isOpened():
		ret, frame = camera.read()
		if not ret: continue

		# Check if there is a hand
		first = second = False


		# <--- Frame
		frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
		results = hands.process(frame)


		# <--- Hands
		pos = []

		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
		if results.multi_hand_landmarks:

			first = True

			if ( len(results.multi_hand_landmarks) > 1 ): second = True

			if (first):
				for hand_landmarks_first in [results.multi_hand_landmarks[0]]:
					mp_drawing.draw_landmarks(
	            			frame, 
	            			hand_landmarks_first, 
	            			mp_hands.HAND_CONNECTIONS
	            		)

				for id, landmark in enumerate(hand_landmarks_first.landmark):
					h, w, c = frame.shape
					pos.append([int(landmark.x*w), int(landmark.y*h)])


		# <--- Left/Right
		# Check if right hand in first array
		# Compare bottom point and thumb base with each other
		# If bottom western than thumb then it is a left hand 
		#  and they have to be swiped
		isRight = isLeft = False
		letter_pos = []
		enter_pos = []
		if (first):

			if (not second):
				if (pos[0][0] > pos[1][0]):   # Right hand
					letter_pos = pos
					isRight = True

					for hand_landmarks_first in [results.multi_hand_landmarks[0]]:
						mp_drawing.draw_landmarks(
		            			frame, 
		            			hand_landmarks_first, 
		            			mp_hands.HAND_CONNECTIONS,
			            		mp_drawing_styles.
		            				get_default_hand_landmarks_style()
		            		)

				else:
					enter_pos = pos
					isLeft = True


			else:
				isRight = isLeft = True
				h, w, c = frame.shape
				
				if (pos[0][0] > pos[1][0]):   # Left hand
					letter_pos = pos

					for hand_landmarks_first in [results.multi_hand_landmarks[0]]:  # Make right hand with rainbow markers 
						mp_drawing.draw_landmarks(
		            			frame, 
		            			hand_landmarks_first, 
		            			mp_hands.HAND_CONNECTIONS,
		            			mp_drawing_styles.
	            					get_default_hand_landmarks_style()
		            		)

					for hand_landmarks_second in [results.multi_hand_landmarks[1]]: # Make left hand with ordinary markers 
						mp_drawing.draw_landmarks(
		            			frame, 
		            			hand_landmarks_second, 
		            			mp_hands.HAND_CONNECTIONS
		            		)

					for id, landmark in enumerate(hand_landmarks_second.landmark):
						enter_pos.append([int(landmark.x*w), int(landmark.y*h)])

				else:
					enter_pos = pos

					for hand_landmarks_first in [results.multi_hand_landmarks[0]]: # Make left hand with ordinary markers 
						mp_drawing.draw_landmarks(
		            			frame, 
		            			hand_landmarks_first, 
		            			mp_hands.HAND_CONNECTIONS
		            		)

					for hand_landmarks_second in [results.multi_hand_landmarks[1]]: # Make right hand with rainbow markers 
						mp_drawing.draw_landmarks(
		            			frame, 
		            			hand_landmarks_second, 
		            			mp_hands.HAND_CONNECTIONS,
		            			mp_drawing_styles.
	            					get_default_hand_landmarks_style()
		            		)

					for id, landmark in enumerate(hand_landmarks_second.landmark):
						letter_pos.append([int(landmark.x*w), int(landmark.y*h)])



		cmd = ""
		# <--- Poses
		# Figure out poses for hand
		if (isRight): letter = F.letterFingers(letter_pos)

		if (isLeft): cmd = F.enterFinger(enter_pos)


		# <--- Text
		if (isRight):
			position = (int(cam_Width//2)-30, int(cam_Height*.9))
			printText ( letter, position, 2, False )

		if (isLeft):
			if (add and cmd != "-" and cmd != "DEFAULT"):
				add = False

				if (cmd == "ERASE"):
					string = string[:-1]

				if (canWrite):
					if (cmd == "ENTER"): 
						if (letter != "-"):
							string += letter

					elif (cmd == "SPACE" and len(string) > 0):
						if (string[-1] != " "):
							string += " "

					elif (cmd == "POINT"):
						string += "."

					elif (cmd == "COMMA"):
						string += ","

					elif (cmd == "QUESTION"):
						string += "?"

					elif (cmd == "EXPLANATION"):
						string += "!"


			elif (not add and cmd == "DEFAULT"):
				restartGo = True
				add = True

			elif (cmd == "ERASE" and len(string) > 0):
				if (restartGo):
					restartGo = False
					timeSave = int(time.time())
				
				if (int(time.time()) - timeSave >= restartTime):
					restartString()

				elif (int(time.time()) - timeSave >= restartTime-3):
					startPulsing()


		position = (0, 30)

		stick += 1
		if (stick <= animationSpeed):
			printText ( string + "|", position, 35, True )
		elif (stick <= animationSpeed * 2):
			printText ( string, position, 35, True )
		else:
			stick = 0
			printText ( string, position, 35, True )


		# <--- Show
		cv2.imshow(cameraName, frame)
		

		# <--- Close
		if cv2.waitKey(5) & 0xFF == 27: break


# ---------- Exit
camera.release()
cv2.destroyAllWindows()
cv2.waitKey(10)