#! /usr/bin/env python
# -*- coding: utf-8 -*-
# external depdendencies
import numpy as np
from std_msgs.msg import Float32
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import rospy
from math import pi as PI
import PID

class Control_Module:

    def __init__(self,picDims,gains,outLimits,intLimits,rate):
        # compute PID Reference Point
        self.frameWidth = picDims[0]
        self.frameHeight = picDims[1]
        self.ref = self.frameWidth/2

        # get important information from the vision Module
        self.coordListener=rospy.Subscriber("/centerCoordinatesTransmition",String,self.coordCallback)
        self.numColorListener = rospy.Subscriber("/num_red",Float32,self.numRedCallback)

        # vision module placeholders
        self.colorP = 0.0
        self.centerCoord = [self.ref,-1]

        # publish message to make the robot move
        self.velocityPub = rospy.Publisher("/cmd_vel",Twist,queue_size=1)

        # Control Stuff
        self.pid = PID.PID_Controller(gains,self.ref,intLimits,outLimits)
        self.rate = rospy.Rate(rate)


    # fetch line's center coordinates (PID Feedback)
    def coordCallback(self,msg):
        msg = str(msg)
        msg = msg.split()
        x = msg[1][1:]
        y = msg[3][:-1]
        cord = [float(x),float(y)]
        self.centerCoord = cord

    # Get colorPercentage (to stop de car)
    def numRedCallback(self,msg):
        self.colorP = msg.data

    def direction(self,x):
        diff = self.ref-x
        if(diff > 0):
            return -1.0
        else:
            return 1.0


    # generate a twist message to move the robot 
    def nextMovement(self):
        moveMsg = Twist()
        
        if (self.colorP > 17.5):
            moveMsg.linear.x = 0.0
            moveMsg.angular.z = 0.0
        else:
            moveMsg.linear.x = 0.2
            xCord = self.centerCoord[0]
            err = xCord - self.frameWidth/2
            moveMsg.linear.x = 0.2
            moveMsg.angular.z = -float(err) / 350

        

        return moveMsg

    # publish a move message
    def moveRobot(self):
        moveMsg = self.nextMovement()
        self.velocityPub.publish(moveMsg)
        self.rate.sleep()

if __name__ == "__main__":
    rospy.init_node("Control_Module")
    picDims = [640,480]
    rate = 40
    intLimits = [10,1000]
    outLimits = [-900,900]
    gains = [1,5,4]
    controlModule = Control_Module(picDims,gains,outLimits,intLimits,rate)    

    while not rospy.is_shutdown():
        controlModule.moveRobot()
        controlModule.rate.sleep()
        if rospy.is_shutdown():
            break