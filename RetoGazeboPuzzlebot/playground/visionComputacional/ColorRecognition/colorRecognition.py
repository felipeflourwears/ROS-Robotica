#! /usr/bin/env python
# -*- coding: utf-8 -*-


import cv2
import numpy as np




path = "/home/luis/Documents/Reto_Mio/playground/visionComputacional/ColorRecognition/resources/red2.png"

lowerRed = np.array([120,0,0])
upperRed = np.array([255,20,20])

image = cv2.imread(path)
imageCopy = np.copy(image)
imageCopy = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2RGB)
imageCopy = cv2.resize(imageCopy,(640,480))
mask = cv2.inRange(imageCopy, lowerRed, upperRed)
numRed = np.sum(mask == 255)

print("numRed",numRed)
print(imageCopy.shape)
percentage = (numRed*3/(480*640))*100
print(percentage)

cv2.imshow('mask',mask)
cv2.imshow('image',imageCopy)

cv2.waitKey(0)