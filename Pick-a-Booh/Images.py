# ---------- Imports
import cv2
import numpy as np


# ---------- Defs
def resizeImage(image, cam_Width, cam_Height):
	imWidth = image.shape[1]
	imHeight = image.shape[0]

	#maximumSize = int(F.size(allPos) * 10)

	maximumSize = cam_Height // 3
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

	for i in range( len(images) ):
		image = cv2.imread("Images/" + images[i])
		resized = resizeImage(image, cam_Width, cam_Height)

		x = 40 * i + 10
		y = 40 * i + 10

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

		places.append([images[i], [x, resized.shape[1]+x], [y, resized.shape[0]+y], False])
		screenImages.append([rows, cols, mask_inv, img2_fg])