import cv2
import numpy as np
import matplotlib.pyplot as plt

filePath = 'Images/Darth-Vader.jpeg'
img = cv2.imread(filePath, 1)
reversed_image = img[:, :, ::-1]
# plt.imshow(img)
cv2.imshow('Image', reversed_image)
# cv2.imshow('HSV', cv2.cvtColor(reversed_image, cv2.COLOR_RGB2HSV))

cv2.waitKey(0) 
cv2.destroyAllWindows() 