# ----- Imports
import cv2
from random import randint
import numpy as np
import math


# ----- Defs
def get_noice():
    _x = _y = 0
    A = B = 0
    
    for i in range(len(points)):
        x = points[i][0]
        y = points[i][1]
        
        _x += x
        _y += y
        
        A += (x * y)
        B += (x * x)
        
    n = len(points)
    a_h = (_y*_x - n*A) / (_x*_x - n*B)
    b_h = (_y - _x*a_h) / n
    
    return [a_h, b_h]
        

# ----- Variables
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500
WINDOW_NAME = 'Points'

points = []

img = cv2.imread("line.jpg")
img = cv2.resize(img, (WINDOW_HEIGHT, WINDOW_WIDTH))


# ----- Main
        
# Get border        
border = 255 - cv2.inRange(img, (140,0,0), (255,255,255))
border = cv2.morphologyEx(border, cv2.MORPH_OPEN, kernel=np.ones((3,3), np.uint8))

right = down = 0
left = up = WINDOW_WIDTH

output = cv2.connectedComponentsWithStats(border, 4, cv2.CV_32S)
num_labels = output[0]
stats = output[2]

for i in range (num_labels):
    a = stats[i, cv2.CC_STAT_AREA]
    t = stats[i, cv2.CC_STAT_TOP]
    l = stats[i, cv2.CC_STAT_LEFT]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]


    if (a < 500):
        left = min(left, l)
        right = max(right, l)
        
        up = min(up, t)
        down = max(down, t)

        
crop = img[left:right, up:down]
     
# Find points
mask = 255 - cv2.inRange(crop, (0,0,140), (255,255,255))

output = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
num_labels = output[0]
stats = output[2]

for i in range (num_labels):
    a = stats[i, cv2.CC_STAT_AREA]
    t = stats[i, cv2.CC_STAT_TOP]
    l = stats[i, cv2.CC_STAT_LEFT]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]


    if (a < 500):
        #cv2.rectangle(crop, (l, t), (l + w, t + h), (255, 0, 255), 1)
        points.append([l, t])
        
# Draw a line
a = get_noice()[0]
b = get_noice()[1]

x0 = 0
y0 = b
x = WINDOW_WIDTH
y = a*x + b
cv2.line(crop, (int(x0), int(y0)), (int(x), int(y)), color=(0,0,0), thickness=2)

img[left:right, up:down] = crop

cv2.imshow(WINDOW_NAME, img)


# ----- Exit
if cv2.waitKey(0) == ord('q'):
    cv2.destroyWindow(WINDOW_NAME)