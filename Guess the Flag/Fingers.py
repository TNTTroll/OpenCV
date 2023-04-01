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

# Count all NOT bended fingers
# Return the number
def countFingers(allPos):
	count = 5

	for x in range(5):
		if ( isBend(fingerNames[x], allPos) ): 
			count -= 1

	return count


# ---------- Defs
# Return the pose for the hand
def poseFingers(allPos):
	pose = 'None'
	count = countFingers(allPos)

	if ( count == 2 and not isBend("Index", allPos) and not isBend("Thumb", allPos) ):
		pose = "Pick"

	elif ( count == 2 and not isBend("Thumb", allPos) and not isBend("Pinky", allPos)):
		pose = "Skip"

	return pose

# Check if the finger touch the "Start" ball
def wasCaught(finger, ballPos, radius):
	distance = distanceBtw(finger, [ballPos[0], ballPos[1]])

	if ( distance < radius ): return True

	return False