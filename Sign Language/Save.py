# ---------- Imports
import cv2
import mediapipe as mp
from time import sleep

import Fingers as F


# ---------- Variables
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

cam_Width = 640
cam_Height = 480

cameraName = "Camera"

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)

size = 20

string = ""
add = True


# ---------- Settings
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)


# ---------- Defs
def printText(text, position, color):
	text = str(text)
	cv2.rectangle(frame, (position[0]-size, position[1]-size*2), 
						 (position[0]+size*4, position[1]+size), black, -1)
	cv2.putText(frame, text, (position[0], position[1]), 
				cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)


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

			if (second):
				isRight = isLeft = True
				
				if (pos[0][0] > pos[1][0]):   # Left hand
					letter_pos = pos

					for hand_landmarks_first in [results.multi_hand_landmarks[0]]:
						mp_drawing.draw_landmarks(
		            			frame, 
		            			hand_landmarks_first, 
		            			mp_hands.HAND_CONNECTIONS,
		            			mp_drawing_styles.
	            					get_default_hand_landmarks_style()
		            		)
						
					for hand_landmarks_second in [results.multi_hand_landmarks[1]]:
						mp_drawing.draw_landmarks(
		            			frame, 
		            			hand_landmarks_second, 
		            			mp_hands.HAND_CONNECTIONS
		            		)

					for id, landmark in enumerate(hand_landmarks_second.landmark):
						h, w, c = frame.shape
						enter_pos.append([int(landmark.x*w), int(landmark.y*h)])

				else:
					enter_pos = pos

					for hand_landmarks_first in [results.multi_hand_landmarks[0]]:
						mp_drawing.draw_landmarks(
		            			frame, 
		            			hand_landmarks_first, 
		            			mp_hands.HAND_CONNECTIONS
		            		)

					for hand_landmarks_second in [results.multi_hand_landmarks[1]]:
						mp_drawing.draw_landmarks(
		            			frame, 
		            			hand_landmarks_second, 
		            			mp_hands.HAND_CONNECTIONS,
		            			mp_drawing_styles.
	            					get_default_hand_landmarks_style()
		            		)

					for id, landmark in enumerate(hand_landmarks_second.landmark):
						h, w, c = frame.shape
						letter_pos.append([int(landmark.x*w), int(landmark.y*h)])

			else:
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


		enter = False
		# <--- Poses
		# Figure out poses for hand
		if (isRight): letter = F.letterFingers(letter_pos)

		if (isLeft): enter = F.enterFingers(enter_pos)


		# <--- Text
		if (isRight):
			position = (int(cam_Width//2)-30, int(cam_Height*.9))
			printText ( letter, position, white )

			if (add and enter):
				string += letter
				add = False

				print(string)

			else:
				add = True


		# <--- Show
		cv2.imshow(cameraName, frame)
		

		# <--- Close
		if cv2.waitKey(5) & 0xFF == 27: break


# ---------- Exit
camera.release()
cv2.destroyAllWindows()
cv2.waitKey(10)