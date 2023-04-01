# ---------- Imports
import cv2
import numpy as np
from random import randint
import playsound as ps 


# ---------- Defs
# Play neccessery audio
def playAudio(name):
	ps.playsound(f"Sounds/{name}.wav", block = False)

# Resize an image to fit in the screen
def resizeImage(image, cam_Width, cam_Height):
	imWidth = image.shape[1]
	imHeight = image.shape[0]

	maximumSize = cam_Width // 5
	imageSize = max(imHeight, imWidth)

	height = width = maximumSize
	if (imageSize == imHeight):
		height = maximumSize
		width = int(maximumSize * imWidth / imHeight)
	else:
		height = int(maximumSize * imHeight / imWidth)
		width = maximumSize

	resized = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)

	return resized

# Check if the finger on the image
def getImage(places, allPos):
	pick = "None"
	fX = allPos[8][0]
	fY = allPos[8][1]

	for image in places:
		if (fX > image[1][0] and fX < image[1][1] and
			fY > image[2][0] and fY < image[2][1]):
			pick = image
			break

	return pick

# Def for show an image on the screen
# Get palm's position and place an image between three bases of: palm, pinky and index
def openMainImage(frame, images, places, screenImages, cam_Width, cam_Height):

	lenght = len(images) - 1
	picked = []
	while ( len(set(picked)) != 4):
		picked = [randint(0, lenght) for x in range(4) ]

	for i in range(4):
		image = cv2.imread("Images/" + images[picked[i]])
		resized = resizeImage(image, cam_Width, cam_Height)

		x = cam_Width // 4 * i + 15
		y = cam_Height // 10 * 9 - (resized.shape[0] // 2) - 10 

		move = np.float32([ [1, 0, x],
	                        [0, 1, y],
	                        [0, 0, 1] ])

		adding = cv2.warpPerspective(resized, move, (cam_Width, cam_Height))

		rows,cols,channels = adding.shape
		roi = frame[0:rows, 0:cols]

		img2gray = cv2.cvtColor(adding, cv2.COLOR_BGR2GRAY)
		ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
		mask_inv = cv2.bitwise_not(mask)

		img2_fg = cv2.bitwise_and(adding, adding, mask = mask)

		places.append([images[picked[i]], [x, resized.shape[1]+x], [y, resized.shape[0]+y], False])
		screenImages.append([rows, cols, mask_inv, img2_fg])

	name = images[picked[randint(0, 3)]]
	return name[0:name.rfind(".")]