# ----- Imports
import cv2
import numpy as np


# ----- Defs
def nothing(v): pass


def me_texting(frame, text):
	cv2.putText(frame, str(text), (10, frame.shape[0]-20), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 4, cv2.LINE_AA)
	cv2.putText(frame, str(text), (10, frame.shape[0]-20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)


def me_processing(frame):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)
	
	lut = (255*np.tanh(vibrance*xval/255)/np.tanh(1)+0.5).astype(np.uint8)
	new_s = cv2.LUT(s,lut)
	new_hsv = cv2.merge([h,new_s,v])
	vib = cv2.cvtColor(new_hsv,  cv2.COLOR_HSV2BGR)

	processing = cv2.addWeighted(vib, contrast, np.zeros(vib.shape, vib.dtype), 0, brightness)
	processing = cv2.filter2D(processing, int(sharpness), kernel_vib)

	return processing


def me_coloring(frame):
	mask = cv2.inRange(frame, (b_min, g_min, r_min), (b_max, g_max, r_max))

	return mask


def me_cropping(frame):
	crop = frame[up:up+down, left:left+right]

	return crop


def me_morphing(frame):
	morph = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel = np.ones((5, 5),np.uint8), iterations = 1)
	morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel = np.ones((2, 2),np.uint8), iterations = 1)
	morph = cv2.dilate(morph, kernel = np.ones((17, 17),np.uint8), iterations = 3)

	return morph


def me_connecting(frame):
	connect = frame.copy()
	output = cv2.connectedComponentsWithStats(morph, 4, cv2.CV_32S)
	num_labels = output[0]
	stats = output[2]
	
	maxi = [0, 0, 0, 1, 1]
	for i in range (1, num_labels):
	    a = stats[i, cv2.CC_STAT_AREA]
	    t = stats[i, cv2.CC_STAT_TOP]
	    l = stats[i, cv2.CC_STAT_LEFT]
	    w = stats[i, cv2.CC_STAT_WIDTH]
	    h = stats[i, cv2.CC_STAT_HEIGHT]

	    if (a > maxi[0]):
	    	maxi = [a, t, l, w, h]
	
	cv2.rectangle(connect, (maxi[2]+left, maxi[1]+up), (maxi[2] + maxi[3] + left, maxi[1] + maxi[4] + up), (255, 0, 255), 1)

	return connect, maxi


def get_noise(points):
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


def find_line(frame, img, border, connect):
    points = []
    

    mask = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel = np.ones((5, 5),np.uint8), iterations = 1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel = np.ones((2, 2),np.uint8), iterations = 1)

    output = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    num_labels = output[0]
    stats = output[2]

    for i in range (1, num_labels):
    	points.append([stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]])

    draw = frame.copy()[border[1]+up+10:border[1]+border[4]+up-10, border[2]+left:border[2]+border[3]+left]
    if (len(points) > 10):
        a = get_noise(points)[0]
        b = get_noise(points)[1]

        x0 = 0
        y0 = b
        x = draw.shape[1]
        y = a*x + b
        cv2.line(draw, (int(x0), int(y0)), (int(x), int(y)), color=(0,0,0), thickness=2)

        for i in range(len(points)):
        	cv2.rectangle(connect, (points[i][0]+border[2]+left, points[i][1]+border[1]+up+10), 
        				 (points[i][0] + points[i][2] + border[2] + left, points[i][1] + points[i][3] + border[1] + up), 
        				 (255, 0, 255), 1)

    line = frame.copy()
    line[border[1]+up+10:border[1]+border[4]+up-10, border[2]+left:border[2]+border[3]+left] = draw
    return line, connect


# ----- Variables

# <<< Window
WINDOW_SIZE = 2

WINDOW_NAME = "Get a Line"

# <<< Video
video = cv2.VideoCapture("video_line.MOV")

# <<< Processing
contrast = .9
brightness = 100
vibrance = 3
sharpness = -1

xval = np.arange(0, 256)
kernel_vib = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

# <<< Colors
b_min = 0
g_min = 95
r_min = 0
b_max = 212
g_max = 225
r_max = 179

# <<< Cropping
left = 60
right = 435
up = 0
down = 427


# ----- Main
while True:
	ret, frame = video.read()

	if ret:
		frame = cv2.resize(frame, (frame.shape[1] // WINDOW_SIZE, frame.shape[0] // WINDOW_SIZE))

		# <<< Processing
		processing = me_processing(frame)

		# <<< Colors
		mask = me_coloring(processing)

		# <<< Cropping
		crop = me_cropping(mask)

		# <<< Morph
		morph = me_morphing(crop)
		
		# <<< Connection
		connect, border = me_connecting(frame)

		# <<< Find line
		find_area = mask[border[1]+up+10:border[1]+border[4]+up-10, border[2]+left:border[2]+border[3]+left]
		line, connect = find_line(frame, find_area, border, connect)

		# <<< Showing
		me_texting(frame, "Ordinary")
		me_texting(processing, "Processing")
		me_texting(connect, "Detecting")
		me_texting(line, "Line")

		videos_part_1 = np.hstack((frame, processing))
		videos_part_2 = np.hstack((connect, line))

		full_screen = np.vstack((videos_part_1, videos_part_2))

		cv2.imshow(WINDOW_NAME, full_screen)

	else:
		video.set(cv2.CAP_PROP_POS_FRAMES, 0)


	key = cv2.waitKey(0)
	if key == ord("c"):
		continue

	if key == ord('q'):
		break


# ----- Exit
cv2.destroyAllWindows()