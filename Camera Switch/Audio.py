# ------------ Imports
import cv2
import numpy as np
import pyaudio
import sys


# ------------ Variables
cam_Width = 640
cam_Height = 480

cameraName = "Camera"

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_Width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_Height)

cv2.namedWindow(cameraName)


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SENSIVITY = 50
delay = 0

negative = False


# ------------ Settings
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


# ------------ Camera
while True:
    ret, frame = cam.read()

    delay += 1
    
    data = stream.read(CHUNK)
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak = np.average(np.abs(data))*2

    if (int(SENSIVITY*peak/2**16) > 0):
        if (delay >= 30):
            negative = not negative
            delay = 0

    if (negative):
        frame = 255 - frame


    cv2.imshow(cameraName, frame)


    k = cv2.waitKey(10) & 0xFF
    if ((not ret) or (k == ord('q') or k == ord('й'))):
        break


# ------------ Exit
cam.release()
cv2.destroyAllWindows()
cv2.waitKey(10)

stream.stop_stream()
stream.close()
p.terminate()