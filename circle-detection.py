import cv2 as cv
import numpy as np
import time

videoCapture = cv.VideoCapture(0)

prevFrameTime = 0
newFrameTime = 0

while True:
    ret, frame = videoCapture.read()
    if not ret: break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

    circles = cv.HoughCircles(grayFrame, cv.HOUGH_GRADIENT, 1.2, 100)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv.circle(frame, (x, y), 5, (0, 128, 255), -1)

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