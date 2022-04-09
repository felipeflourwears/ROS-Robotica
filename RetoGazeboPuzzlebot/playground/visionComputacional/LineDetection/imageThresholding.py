# -*- coding: utf-8 -*-


import cv2
import numpy as np
import matplotlib.pyplot as plt


height = 640
width = 480

path = "/home/luis/Documents/Reto_Mio/playground/visionComputacional/LineDetection/resources/line1.png"


# method 1 in imageProccessing
image = cv2.imread(path)
imageCopy = np.copy(image)
imageCopy = cv2.resize(imageCopy,(height,width)) 
imageCopy = cv2.GaussianBlur(imageCopy,(7,7),cv2.BORDER_DEFAULT)
blurry = cv2.cvtColor(imageCopy,cv2.COLOR_RGB2GRAY)


# method 2 cut the image
slice = blurry[325:,:]
retval, binary = cv2.threshold(slice, 127, 255, cv2.THRESH_BINARY)
# center of the binarized area (way)
contours, hierarchy = cv2.findContours(binary,1,cv2.CHAIN_APPROX_NONE)
C = max(contours,key= cv2.contourArea)
M = cv2.moments(C)
cx = int(M["m10"]/M["m00"])
cy = int(M["m01"]/M["m00"])

print(cx,cy)


cv2.circle(binary,(cx,cy),5,color=0,thickness=2)


cv2.imshow('gray',binary)
cv2.waitKey(0)
cv2.destroyAllWindows()

