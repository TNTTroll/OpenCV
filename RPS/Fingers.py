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
	pose = 'None'
	count = countFingers(allPos)

	if ( count == 5 ):
		pose = "Paper"

	elif ( count == 2 and 
		   not isBend("Index", allPos) and 
		   not isBend("Middle", allPos) ):
		pose = "Scissors"

	elif ( count == 0 ):
		pose = "Rock"

	return pose


# ---------- Logic
# Get two poses to compare them
# Return WINNER or DRAW
def winner(pose1, pose2):
	if (pose1 == pose2 or pose1 == "None" or pose2 == "None"):
		return "Draw"

	if (pose1 == "Rock"):
		if (pose2 == "Paper"):
			return "Second"
		else: return "First"

	if (pose1 == "Scissors"):
		if (pose2 == "Rock"):
			return "Second"
		else: return "First"

	if (pose1 == "Paper"):
		if (pose2 == "Scissors"):
			return "Second"
		else: return "First"