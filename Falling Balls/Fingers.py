# ---------- Imports
from math import sqrt


# ---------- Helpers
# Get distance between two points on the screen
def distanceBtw(pos1, pos2):
	return sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 )


# ---------- Logic
# Check if finger colider is in a ball's one
def wasCaught(finger, ballPos, radius):

	distance = distanceBtw(finger, [ballPos[0], ballPos[1]])

	if ( distance < radius ):
		return True

	return False
