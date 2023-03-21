# ---------- Imports
from random import randint
import playsound as ps


# ---------- Helpers
# Play neccessery audio
def playAudio(name):
	ps.playsound(f"Sounds/{name}.wav", block = False)


# ---------- Game
# Get random spot on the top of the screen and spawn there a ball
def spawnBall(ballPos, cam_Width, cam_Height):

	playAudio("Coin")

	ballPos = [randint(cam_Width//15, cam_Width//15*14), 10]
	return ballPos

# Check if the balll out of the screen
def ballOutOfLimits(ballPos, cam_Height):
	if (ballPos[1] > cam_Height):
		return True
	return False





