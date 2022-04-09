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
imageCopy = cv2.GaussianBlur(imageCopy,(5,5),cv2.BORDER_DEFAULT)
canny = cv2.cvtColor(imageCopy,cv2.COLOR_RGB2GRAY)
canny = cv2.Canny(canny,125,175)


# Method 2 in line detection (for detecting the lines and correct the robot's trayectory)
retval, binary = cv2.threshold(canny, 127, 255, cv2.THRESH_BINARY)
contours,hierchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contourImage = np.copy(imageCopy)
contourImage = cv2.drawContours(contourImage,contours,-1,(0,0,255),2)


 
# Method 3: Slice contour image and return the center line 190:390
contourImage = contourImage[300:-10,:,:]
print(contourImage.shape)



# Method 3 for classification (where is the line and where it is not)

kMeansImage = np.copy(image)
kMeansImage = cv2.cvtColor(kMeansImage,cv2.COLOR_BGR2HSV)
kMeansImage = cv2.resize(kMeansImage,(height,width)) 

pixelVals = kMeansImage.reshape((-1,3))
pixelVals = np.float32(pixelVals)

criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 10, 0.2)
k = 5
retval, labels, centers = cv2.kmeans(pixelVals, k, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS)

# convert data into 8-bit values
centers = np.uint8(centers)
segmented_data = centers[labels.flatten()]

# reshape data into the original image dimensions
segmented_image = segmented_data.reshape((kMeansImage.shape))
labels_reshape = labels.reshape(kMeansImage.shape[0], kMeansImage.shape[1])


#plt.imshow(segmented_image)
#plt.show()


cluster = 1 # the first cluster

masked_image = np.copy(kMeansImage)
# turn the mask green!
masked_image[labels_reshape == cluster] = [234, 255, 12]

#cv2.imshow('Kmeans',masked_image)
cv2.imshow('contour',contourImage)




#cv2.imshow('contour',contourImage)
#cv2.imshow('Kmeans',kMeansImage)


cv2.waitKey(0)
cv2.destroyAllWindows()
