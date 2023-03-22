# ---------- Imports
from math import sqrt


# ---------- Variables
fingerNames = [ "Thumb", "Index", "Middle", "Ring", "Pinky"]


# ---------- Helpers
# Get distance between two points on the screen
def distanceBtw(pos1, pos2):
	return sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 )


# Check if the finger is bended or not
# Return TRUE if bend; FALSE if not bend
def isBend(tipName, position):
	ind = (fingerNames.index(tipName) + 1) * 4
	
	if (ind != 4):
		if ( distanceBtw(position[ind], position[0]) < distanceBtw(position[ind-2], position[0]) ):
			return True

	else:
		if ( position[1][0] < position[0][0] ):   			# Right hand
			if ( position[ind][0] > position[ind-2][0] ):
				return True

		else:    											# Left hand 
			if ( position[ind][0] < position[ind-2][0] ):
				return True

	return False 


# ---------- Defs
# Count all NOT bended fingers
# Return the number
def countFingers(allPos):
	count = 5

	for x in range(5):
		if ( isBend(fingerNames[x], allPos) ): 
			count -= 1

	return count


# Return the pose for the hand
def poseFingers(allPos):
	pose = ''
	count = countFingers(allPos)

	if ( count == 5 ):
		pose = "Default"

	elif ( count == 4 and isBend("Thumb", allPos) ):
		pose = "Forward"

	elif ( count == 1 and not isBend("Thumb", allPos) ):
		pose = "Backward"

	elif ( count == 4 and isBend("Index", allPos) ):
		pose = "Zoom in"

	elif ( count == 4 and isBend("Middle", allPos) ):
		pose = "Zoom out"

	elif ( count == 0 ):
		pose = "Close"


	return pose


# Get the maximum size of the image
# Get distance between palm's base and pinky's base as constant
def size(allPos):
	distance = distanceBtw( allPos[0], allPos[17] ) // 4

	return max(distance, 1)