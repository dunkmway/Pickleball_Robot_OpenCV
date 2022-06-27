import cv2 as cv
import numpy as np
import time

videoCapture = cv.VideoCapture(0)
prevCircle = None
dist = lambda x1, y1, x2, y2: (x1-x2)**2 + (y1-y2)**2

prevFrameTime = 0
newFrameTime = 0

while True:
    ret, frame = videoCapture.read()
    if not ret: break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=30, minRadius=75, maxRadius=400)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                    chosen = i
            cv.circle(frame, (i[0], i[1]), 1, (0,100,100), 3)
            cv.circle(frame, (i[0], i[1]), i[2], (255,0,255), 3)

        # cv.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 3)
        # cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,255), 3)
        prevCircle = chosen

    newFrameTime = time.time()
    fps = 1/(newFrameTime - prevFrameTime)
    prevFrameTime = newFrameTime
    fps = int(fps)
    fps = str(fps)

    flipFrame = cv.flip(frame, 1)
    cv.putText(flipFrame, 'fps: ' + fps, (7, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv.LINE_AA)
    cv.imshow('circles', flipFrame)

    if cv.waitKey(1) & 0xff == ord('q'): break

videoCapture.release()
cv.destroyAllWindows()