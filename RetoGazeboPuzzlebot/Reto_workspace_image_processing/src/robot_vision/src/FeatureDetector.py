#! /usr/bin/env python
# -*- coding: utf-8 -*-


import cv2

import numpy as np

import rospy, cv_bridge

from sensor_msgs.msg import Image

from std_msgs.msg import Float32


class FeatureDetector:
    def __init__(self,height,width):
        #self.frameWidth = 640
        #self.frameHeight = 480
        self.frameWidth = width
        self.frameHeight = height
        self.total = self.frameHeight * self.frameWidth

    # given particular frame, slices it in order to keep only the robot's path and obtains the border's coordinates
    # Important: the input must be a hsv image
    def findPathCenterCoordinates(self,mask,dimentions):
        h, w, d = dimentions
        search_top = 3*h/4
        search_bot = 3*h/4 + 20
        search_top = int(3*h/4)
        search_bot = int(3*h/4 + 20)
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        M = cv2.moments(mask)
        try:
            cx, cy = M['m10']/M['m00'], M['m01']/M['m00']
        except ZeroDivisionError:
            cy, cx = h/2, w/2
        return [cx,cy]
        """
        slice = image[325:,:]
        # grayscale pixels beyond 127 will be defaulted to white (255) otherwise they will be defaulted to black
        retval, binary = cv2.threshold(slice, 150, 255, cv2.THRESH_BINARY)
        # center of the binarized area (way)
        contours, hierarchy = cv2.findContours(binary,1,cv2.CHAIN_APPROX_NONE)[-2:]    # get only the last two parameters    
        C = max(contours,key= cv2.contourArea)
        M = cv2.moments(C)
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        return [cx,cy]
        """