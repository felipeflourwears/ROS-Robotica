#! /usr/bin/env python
# -*- coding: utf-8 -*-

# external depdendencies
import cv2

import numpy as np

import rospy, cv_bridge

from sensor_msgs.msg import Image

from std_msgs.msg import Float32
from std_msgs.msg import String
# my classes
import CameraControl 
import FeatureDetector 
import ImageProcessing 




# General Robot Vision Module
class RobotVision:
    def __init__(self,width,height,inputRate):
        # image dimentions
        self.frameWidth = width
        self.frameHeight = height
        self.total = self.frameHeight * self.frameWidth
        # esential computer vision modules
        self.camera = CameraControl.CameraControl()
        self.featDec = FeatureDetector.FeatureDetector(self.frameHeight,self.frameWidth)
        self.imageProc = ImageProcessing.ImageProcessing(self.frameHeight,self.frameWidth)

        # publishers & associated stuff (may move to an independent class later)
        self.rate = rospy.Rate(inputRate)
        self.pixelPercentagePub = rospy.Publisher('/num_red', Float32,queue_size=1)
        self.centerCoordinatesPUb = rospy.Publisher('/centerCoordinatesTransmition',String,queue_size=1)


    def fetchImage(self):
        image = self.camera.getImage()
        while image is None:
            image =  self.camera.getImage()
        return image


    def getPixelPercentage(self,lowerBound,upperBound):
        image = self.fetchImage()
        processedImage = self.imageProc.imagePreprosessing(image,blurry = False,rbgEncode = cv2.COLOR_BGR2RGB)
        mask = self.imageProc.createImageMask(processedImage,lowerBound,upperBound)
        numColor = np.sum(mask == 255)
        percentage = ((numColor*1.0)/(self.total))*100.0
        return percentage


    def getCenterLineCoordinates(self,pixelP,lowerBound,upperBound):
        image = self.fetchImage()
        processedImage = self.imageProc.imagePreprosessing(image,blurry=True,rbgEncode = cv2.COLOR_BGR2HSV)
        mask = self.imageProc.createImageMask(image,lowerBound,upperBound)
        # aqui va el metodo para obtener las coordenacas
        if pixelP > 17.5:
            coord = [-1,-1]
        else:
            coord = self.featDec.findPathCenterCoordinates(mask,processedImage.shape)
        return coord


    
    # publishers (will me moved away pretty soon)
    def publishPixelPercentage(self,pixelP):
        self.pixelPercentagePub.publish(pixelP)

    def publishLineCentralCoordinates(self,pixelP,lowerBound,upperBound):
        cord = self.getCenterLineCoordinates(pixelP,lowerBound,upperBound)
        #rospy.loginfo(cord)
        msg = "{} | {}"
        msg = msg.format(cord[0],cord[1])
        self.centerCoordinatesPUb.publish(msg)


if __name__ == "__main__":

    rospy.init_node("vision_module")
    # RATE
    rate = 40
    # PIXEL COLOR DETECTION RGB BOUNDS
    lowerRed = np.array([120,0,0]) 
    upperRed = np.array([255,20,20])
    # PICEL CENTER COORDINATES DETECTION IN HSV 
    lower_white = np.array([0,0,220])
    higher_white = np.array([255,255,255])
    # FRAME DIMENTIONS 
    frameHeight = 480
    frameWidth = 640

    # VISION MODULE INSTANCE
    visionModule = RobotVision(frameWidth,frameHeight,rate)

    while not rospy.is_shutdown():
        percentage = visionModule.getPixelPercentage(lowerRed,upperRed)
        visionModule.publishPixelPercentage(percentage)
        #coord = visionModule.getCenterLineCoordinates(percentage)
        visionModule.publishLineCentralCoordinates(percentage,lower_white,higher_white)
        visionModule.rate.sleep()