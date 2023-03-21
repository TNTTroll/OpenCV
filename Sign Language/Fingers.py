# ---------- Imports
from math import sqrt


# ---------- Variables
fingerNames = [ "Thumb", "Index", "Middle", "Ring", "Pinky"]


# ---------- Helpers
# Get distance between two points on the screen
def distanceBtw(pos1, pos2):
	return sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 )


# Return id of a finger
def tip(name):
	return (fingerNames.index(name) + 1) * 4


# Check if fingers is bended or not
# Return TRUE if bend; FALSE if not bend
def isBend(tipNames, position):
	for x in range(len(tipNames)):
		if ( not isBendOne(tipNames[x], position) ):
			return False

	return True

def isBendOne(tipName, position):
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


# Check if fingers is bended or not
# Return FALSE if bend; TRUE if not bend
def isStr(tipNames, position):
	for x in range(len(tipNames)):
		if ( not isStrOne(tipNames[x], position) ):
			return False

	return True

def isStrOne(tipName, position):
	return not isBendOne(tipName, position)


# Count all NOT bended fingers
# Return the number
def countFingers(allPos):
	count = 5

	for x in range(5):
		if ( isBendOne(fingerNames[x], allPos) ): 
			count -= 1

	return count


# ---------- Coordination
# Check if two point are close to each other
# "Close" is the size from bottom palm to pinky base divided by two
def isClose(first, second, allPos):

	step = distanceBtw( allPos[0], allPos[17] ) // 2
	
	distance = distanceBtw( allPos[first], allPos[second] )

	if ( distance < step ): return True
	return False

def isFar(first, second, allPos):
	return not isClose(first, second, allPos)


# Check if one point higher than another one 
def higher(first, second, allPos):

	if ( allPos[first][1] < allPos[second][1] ): return True
	return False

def lower(first, second, allPos):
	return not higher(first, second, allPos)


# Check if one point more to left than another one 
def left(first, second, allPos):

	if ( allPos[first][0] < allPos[second][0] ): return True 
	return False

def right(first, second, allPos):
	return not left(first, second, allPos)


# ---------- Hands
# Return the command for the left hand
def enterFinger(p):
	c = countFingers(p)
	cmd = ""

	if ( c == 0 ):
		cmd = "ENTER"

	elif ( c == 2 and isStr(["Thumb", "Index"], p) ):
		cmd = "SPACE"

	elif ( c == 4 and isBend(["Thumb"], p) ):
		cmd = "ERASE"

	elif ( c == 4 and isBend(["Index"], p) ):
		cmd = "POINT"

	elif ( c == 4 and isBend(["Middle"], p) ):
		cmd = "COMMA"

	elif ( c == 4 and isBend(["Ring"], p) ):
		cmd = "QUESTION"

	elif ( c == 4 and isBend(["Pinky"], p) ):
		cmd = "EXPLANATION"

	elif ( c == 5 ):
		cmd = "DEFAULT"

	else:
		cmd = "-"

	return cmd


# Return the letter for the right hand
def letterFingers(p):
	letter = ""
	c = countFingers(p)

	if ( c == 1 and higher(tip("Thumb"), tip("Index"), p) and left(tip("Thumb"), tip("Index")-2, p) and isStr(["Thumb"], p) ):
		letter = "A"

	elif ( c == 4 and isBend(["Thumb"], p) ):
		letter = "B"

	elif ( c == 5 and lower(tip("Thumb"), tip("Index"), p) and isClose(tip("Index"), tip("Index")-2, p) and isClose(tip("Middle"), tip("Middle")-2, p) ):
		letter = "C"

	elif ( c == 1 and left(tip("Index"), tip("Ring")-3, p) and higher(tip("Index"), tip("Index")-1, p) and isStr(["Index"], p) ):
		letter = "D"

	elif ( c == 0 and lower(tip("Thumb"), tip("Index"), p) and isFar(tip("Thumb"), tip("Index"), p) ):
		letter = "E"

	elif ( c == 3 and isBend(["Thumb", "Index"], p) ):
		letter = "F"

	elif ( c == 2 and isClose(tip("Thumb"), tip("Index"), p) and higher(tip("Index"), tip("Pinky")-3, p) and isStr(["Thumb", "Index"], p) ):
		letter = "G"

	elif ( c == 2 and isClose(tip("Index"), tip("Middle"), p) and lower(tip("Middle"), tip("Index"), p) and isStr(["Index", "Middle"], p) ):
		letter = "H"

	elif ( c == 1 and higher(tip("Pinky"), tip("Middle")-2, p) and isStr(["Pinky"], p) ):
		letter = "I"

	elif ( c == 1 and lower(tip("Pinky"), tip("Middle")-2, p) and isStr(["Pinky"], p) ):
		letter = "J"

	elif ( c == 2 and isFar(tip("Index"), tip("Middle"), p) and higher(tip("Thumb"), tip("Ring")-2, p) and isStr(["Index", "Middle"], p) ):
		letter = "K"

	elif ( c == 2 and higher(tip("Index"), tip("Index")-3, p) and isStr(["Thumb", "Index"], p) ):
		letter = "L"

	elif ( c == 0 and right(tip("Thumb"), tip("Ring"), p) and higher(tip("Thumb"), tip("Pinky")-2, p) ):
		letter = "M"

	elif ( c == 0 and right(tip("Thumb"), tip("Middle"), p) and higher(tip("Thumb"), tip("Ring")-2, p) ):
		letter = "N"

	elif ( c == 0 and isClose(tip("Thumb"), tip("Index"), p) and isFar(tip("Thumb"), tip("Ring")-1, p) ):
		letter = "O"

	elif ( c == 3 and lower(tip("Middle"), tip("Thumb"), p) and isStr(["Index", "Middle"], p) ):
		letter = "P"

	elif ( c == 2 and lower(tip("Index"), tip("Pinky")-3, p) and isStr(["Thumb", "Index"], p) ):
		letter = "Q"

	elif ( c == 2 and right(tip("Index"), tip("Middle"), p) and isStr(["Index", "Middle"], p) ):
		letter = "R"

	elif ( c == 0 and isClose(tip("Thumb"), tip("Ring")-1, p) and lower(tip("Thumb"), tip("Pinky")-2, p) ):
		letter = "S"

	elif ( c == 0 and right(tip("Thumb"), tip("Index"), p) and higher(tip("Thumb"), tip("Middle"), p) ):
		letter = "T"

	elif ( c == 2 and isClose(tip("Index"), tip("Middle"), p) and lower(tip("Thumb"), tip("Ring")-2, p) and isStr(["Index", "Middle"], p) ):
		letter = "U"

	elif ( c == 2 and isFar(tip("Index"), tip("Middle"), p) and lower(tip("Thumb"), tip("Ring")-2, p) and isStr(["Index", "Middle"], p) ):
		letter = "V"

	elif ( c == 3 and isStr(["Index", "Middle", "Ring"], p) ):
		letter = "W"

	elif ( c == 1 and isFar(tip("Index"), tip("Middle"), p) and lower(tip("Index"), tip("Index")-1, p) and isStr(["Index"], p) ):
		letter = "X"

	elif ( c == 2 and isStr(["Thumb", "Pinky"], p) ):
		letter = "Y"	

	elif ( c == 1 and right(tip("Index"), tip("Ring")-3, p) and higher(tip("Index"), tip("Index")-1, p) and isStr(["Index"], p) ):
		letter = "Z"

	else:
		letter = "-"


	return letter