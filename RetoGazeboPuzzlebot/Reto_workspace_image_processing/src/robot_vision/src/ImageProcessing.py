#! /usr/bin/env python
# -*- coding: utf-8 -*-


import cv2

import numpy as np

import rospy, cv_bridge

from sensor_msgs.msg import Image

from std_msgs.msg import Float32


class ImageProcessing:
    def __init__(self,height,width):
        #self.frameWidth = 640
        #self.frameHeight = 480
        self.frameWidth = width
        self.frameHeight = height
        self.total = self.frameHeight * self.frameWidth



    def imagePreprosessing(self,image,blurry = False,rbgEncode = cv2.COLOR_BGR2GRAY):
        # creates a copy of the image
        imageCopy = np.copy(image) 
        # resizes by the specified dimentions
        imageCopy = cv2.resize(imageCopy,(self.frameHeight,self.frameWidth))
        # Clan up some noise while increasing the contrast between high frequency regions 
        processed = cv2.GaussianBlur(imageCopy,(7,7),cv2.BORDER_DEFAULT) if blurry == True else imageCopy
        # openCv format transformation
        processed = cv2.cvtColor(imageCopy,rbgEncode)
        return processed

    def createImageMask(self,image,lowerBound,upperBound):
        return  cv2.inRange(image, lowerBound, upperBound)






"""
    def run(self):
        if self.image is None:
            return
        num_red = self.im_proc.getPixelPercentage(self.image)
        #self.im_proc.num_red_pub.publish(num_red)
if __name__ == "__main__":
    rospy.init_node("color_detection")
    cameraControl = CameraControl()
    while not rospy.is_shutdown():
        cameraControl.run()
        cameraControl.rate.sleep()
"""