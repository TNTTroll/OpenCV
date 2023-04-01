# ---------- Imports
import cv2
import mediapipe as mp

import Fingers as F


# ---------- Variables
# <--- Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# <--- Camera
cameraName = "Camera"

cam_Width = 640
cam_Height = 480

# <--- Points
points = []


# ---------- Settings
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)


# ---------- Defs
# Add a point to a line
def addPoint(finger):
	global points

	points.append([finger[0], finger[1]])

# Delete a point from a line
def delPoint():
	global points

	if (len(points) > 0):
		points.pop()

# Draw a whole line on the screen
def drawLine():
	if (len(points) >= 0):
		for i in range(len(points) - 1):
			    cv2.line(frame, (points[i][0], points[i][1]), 
			    	(points[i+1][0], points[i+1][1]), color = (255, 255, 0), thickness = 2)


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


		# <--- Hand
		if (isHand):

			pose = F.poseFingers(land_pos)

			if (pose == "Draw"):
				addPoint(land_pos[8])

			elif (pose == "Erase"):
				delPoint()


		# <--- Line
		drawLine()


		# <--- Show
		cv2.imshow(cameraName, frame)
		

		# <--- Close
		if cv2.waitKey(5) & 0xFF == 27: break


# ---------- Exit
camera.release()
cv2.destroyAllWindows()
cv2.waitKey(10)