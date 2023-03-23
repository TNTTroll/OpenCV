# ---------- Imports
import cv2
import mediapipe as mp

import Fingers as F


# ---------- Variables
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cameraName = "Camera"

cam_Width = 640
cam_Height = 480

size = 20

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)


# ---------- Settings
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)

# ---------- Defs
def printText(text, position, color):
	text = str(text)
	cv2.rectangle(frame, (position[0]-size, position[1]-size*2), 
						 (position[0]+size*5, position[1]+size), black, -1)
	cv2.putText(frame, text, (position[0], position[1]), 
				cv2.FONT_HERSHEY_COMPLEX, .7, color, 2)


# ---------- Main
with mp_hands.Hands(min_detection_confidence=0.5,
    				min_tracking_confidence=0.5) as hands:

	while camera.isOpened():
		ret, frame = camera.read()
		if not ret: continue

		# Check if there are any hands
		first = second = False


		# <--- Frame
		frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
		results = hands.process(frame)


		# <--- Hands
		land_pos_first = []
		land_pos_second = []

		frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
		if results.multi_hand_landmarks:

			first = True

			if ( len(results.multi_hand_landmarks) > 1 ): second = True

			# Draw markers for first hand and save all of its coords
			for hand_landmarks_first in [results.multi_hand_landmarks[0]]:
				mp_drawing.draw_landmarks(
            			frame, 
            			hand_landmarks_first, 
            			mp_hands.HAND_CONNECTIONS
            		)

			for id, landmark in enumerate(hand_landmarks_first.landmark):
				h, w, c = frame.shape
				land_pos_first.append([int(landmark.x*w), int(landmark.y*h)])

			
			# If there is tow hands, 
			# draw markers for second hand and save all of its coords
			if (second):
				for hand_landmarks_second in [results.multi_hand_landmarks[1]]:
					mp_drawing.draw_landmarks(
	            			frame, 
	            			hand_landmarks_second, 
	            			mp_hands.HAND_CONNECTIONS
	            		)

				for id, landmark in enumerate(hand_landmarks_second.landmark):
					h, w, c = frame.shape
					land_pos_second.append([int(landmark.x*w), int(landmark.y*h)])
		

		# <--- Left/Right
		# Check if right hand in first array
		# Compare bottom point and thumb base with each other
		# If bottom western than thumb then it is a left hand 
		#  and they have to be swiped
		if (second):
			if (land_pos_first[0][0] > land_pos_first[1][0]):
				save = land_pos_first
				land_pos_first = land_pos_second
				land_pos_second = save


		# <--- Poses
		# Figure out poses for hand(s)
		if (first): pose_first = F.poseFingers(land_pos_first)

		if (second): pose_second = F.poseFingers(land_pos_second)


		# <--- Text
		if (first):

			if (second):
				# If there are two hand the game will be started
				# Save two poses and compare them to each other
				pos_right = (100, int(cam_Height*.9))
				pos_left = (int(cam_Width*.9)-100, int(cam_Height*.9))

				if (F.winner(pose_first, pose_second) == "First"):
					printText ( pose_first, pos_right, green )
					printText ( pose_second, pos_left, red )

				elif (F.winner(pose_first, pose_second) == "Second"):
					printText ( pose_first, pos_right, red )
					printText ( pose_second, pos_left, green )

				else:
					printText ( pose_first, pos_right, white )
					printText ( pose_second, pos_left, white )

			else:
				# If there is only one hand, it will be shown in white color 
				pos_right = (int(cam_Width//2)-30, int(cam_Height*.9))
				printText ( pose_first, pos_right, white )


		# <--- Show
		cv2.imshow(cameraName, frame)
		

		# <--- Close
		if cv2.waitKey(5) & 0xFF == 27: break


# ---------- Exit
camera.release()
cv2.destroyAllWindows()
cv2.waitKey(10)