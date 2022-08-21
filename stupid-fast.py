# import the necessary packages
from collections import deque
from multiprocessing.dummy import Process
import imutils
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import time
import sys
from operator import itemgetter

prevFrameTime = 0
newFrameTime = 0

beginProcessTime = 0

fps_min = 1000
fps_max = 0
fps_sum = 0
fps_count = 0

process_min = 1000
process_max = 0
process_sum = 0
process_count = 0

def Update_FPS_Total(fps):
	global fps_min
	global fps_max
	global fps_sum
	global fps_count

	if fps < fps_min: fps_min = fps
	elif fps > fps_max: fps_max = fps

	fps_sum += fps
	fps_count += 1

def Update_Process_Total(process):
	global process_min
	global process_max
	global process_sum
	global process_count

	if process < process_min: process_min = process
	elif process > process_max: process_max = process

	process_sum += process
	process_count += 1

def Process_Frame(frame, frameWidth, minRadius, iter, showCircle=False, showMask=False):
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
		#((x, y), radius) = cv2.minEnclosingCircle(c)
		center, radius = cv2.minEnclosingCircle(c)
		#M = cv2.moments(c)
		#center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		#center = (M["m10"] / M["m00"], M["m01"] / M["m00"])
		center = (int(center[0]), int(center[1]))
		radius = round(radius)

		# only proceed if the radius meets a minimum size
		if radius > minRadius:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			if showCircle:
				cv2.circle(frame, center, radius, (255, 0, 0), 1)
				cv2.circle(frame, center, radius, (255, 0, 0), 1)

				cv2.circle(frame, center, 2, (0, 0, 255), -1)
				if showMask:
					cv2.circle(mask, center, radius, (255, 0, 0), 1)
					cv2.circle(mask, center, 2, (0, 0, 255), -1)
			pos = center
	if showMask:
		# cv2.imshow('Mask', mask)
		cv2.imwrite(f"frames/mask_{iters}.jpg", mask)
	return frame, pos	


def Output_Data(frame, index, displayCenter = False, displayFps = False, displayProcess = False, showFrame = False, showFps = False, showProcess = False):
	global prevFrameTime
	global newFrameTime

	#calculate the fps
	newFrameTime = time.perf_counter()
	fps = 1/(newFrameTime - prevFrameTime)
	prevFrameTime = newFrameTime
	fps = int(fps)
	Update_FPS_Total(fps)
	fpsStr = f"fps: {fps} (min: {fps_min}, max: {fps_max}, avg: {fps_sum // fps_count})"
	#fpsStr = 'fps: ' + str(fps).zfill(3) + ' (min: ' + str(fps_min).zfill(3) + ', max: ' + str(fps_max).zfill(3) + ', avg: ' + str(fps_sum // fps_count).zfill(3) + ')'

	# calculate the process time
	endProcessTime = time.perf_counter()
	processTime = (endProcessTime - beginProcessTime) * 1000
	processTime = int(processTime)
	Update_Process_Total(processTime)
	processStr = f"process: {processTime} (min: {process_min}, max: {process_max}, avg: {process_sum // process_count})"
	#processStr = 'process: ' + str(processTime).zfill(3) + ' (min: ' + str(process_min).zfill(3) + ', max: ' + str(process_max).zfill(3) + ', avg: ' + str(process_sum // process_count).zfill(3) + ')'

	positionStr = f"pos: ({center})"
	#positionStr = 'pos: (' + str(int(center[0])).zfill(4) + ', ' + str(int(center[1])).zfill(4) + ')'

	print(positionStr)
	print(fpsStr)
	print(processStr)

	if showFrame:
		# flip the frame to mirror movement
		flipFrame = cv2.flip(frame, 1)
		if showFps:
			# write the fps
			cv2.putText(flipFrame, fpsStr, (7, 28), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
		if showProcess:
			# write the process time
			cv2.putText(flipFrame, processStr, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
		# show the frame to our screen
		# cv2.imshow("Frame", flipFrame)
		cv2.imwrite(f"frames/frame_{index}.jpg", flipFrame)

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
prevFrameTime = time.perf_counter()
iters = 0
loop_start = time.perf_counter()
while iters < 30*10:
	#keep track of processing time
	#beginProcessTime = time.perf_counter()

	# grab the current frame
	frame = vs.read()

	# handle the frame from VideoCapture or VideoStream
	#frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	
	frame, center = Process_Frame(frame, 600, 10, iters, showCircle=False, showMask=False)
	#Output_Data(
	#	frame, 
	#	iters,
	#	displayCenter = True, 
	#	displayFps = True, 
	#	displayProcess = True, 
	#	showFrame = False, 
	#	showFps = False, 
	#	showProcess = False,
	#)
	iters += 1
loop_end = time.perf_counter()
print(f"fps: {iters / (loop_end - loop_start)}, {iters}, {loop_start}, {loop_end}")

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()
