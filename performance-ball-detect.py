# import the necessary packages
import imutils
from imutils.video import VideoStream
import argparse
import cv2
import time
from operator import itemgetter

def Process_Frame(frame, frameWidth, minRadius):
	# frame = imutils.resize(frame, width=frameWidth)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	# mask = cv2.erode(mask, None, iterations=2)
	# mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	# only proceed if at least one contour was found
	pos = (-1, -1)
	if cnts:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		center, radius = cv2.minEnclosingCircle(c)
		center = (int(center[0]), int(center[1]))
		radius = round(radius)

		# only proceed if the radius meets a minimum size
		if radius > minRadius:
			# then update the list of tracked points
			pos = center
	return frame, pos	


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (27, 100, 25)
greenUpper = (38, 240, 220)
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
	frameget = lambda x: x
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
	frameget = itemgetter(1)
# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
iters = 0
loop_start = time.perf_counter()
while iters < 500:
	#keep track of processing time

	# grab the current frame
	frame = vs.read()

	# handle the frame from VideoCapture or VideoStream
	# frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	
	frame, center = Process_Frame(frame, 600, 10)
	iters += 1
loop_end = time.perf_counter()
print(f"fps: {iters / (loop_end - loop_start)}, {iters}")

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()
