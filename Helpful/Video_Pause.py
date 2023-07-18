# Drop detect by OpenCV
# Version 0.1

# ----- Imports
import cv2
import numpy as np


# ----- Defs
def texting(frame, text, x ,y):
	cv2.putText(frame, str(text), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)


# ----- Variables
WINDOW_NAME = "Video"
WINDOW_SIZE = .8

playable = True

video = cv2.VideoCapture("")


# ----- Main
while True:
	if (playable):
		key = cv2.waitKey(30) & 0xFF
	else:
		key = cv2.waitKey(0) & 0xFF
			
	if (key == 32):
		playable = not playable
	elif (key == 99):
		video.set(cv2.CAP_PROP_POS_FRAMES, video.get(cv2.CAP_PROP_POS_FRAMES)-2)
	elif (key == ord('q')):
		break


	ret, frame = video.read()
	
	if ret:
		frame = cv2.resize(frame, (int(frame.shape[1] * WINDOW_SIZE), int(frame.shape[0] * WINDOW_SIZE)))


		texting(frame, video.get(cv2.CAP_PROP_POS_FRAMES), 50, 50)
		
		

		cv2.imshow(WINDOW_NAME, frame)
	
	else:
		video.set(cv2.CAP_PROP_POS_FRAMES, 0)


# ----- Exit
cv2.destroyAllWindows()
cv2.waitKey(10)