#! /usr/bin/env python
# -*- coding: utf-8 -*-


import cv2

import numpy as np

import rospy, cv_bridge

from sensor_msgs.msg import Image

from std_msgs.msg import Float32




class CameraControl:
    def __init__(self):

        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('/camera/image_raw', Image, self.image_callback)
        self.image = None
        #self.rate = rospy.Rate(30)
        #self.im_proc = ImageProcessing()

    # transorms the image from ros to a openCv format
    def image_callback(self, msg):
        self.image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')

    # return the image if available
    def getImage(self):
        return self.image



