#! /usr/bin/env python
# -*- coding: utf-8 -*-
# external depdendencies
import numpy as np
from std_msgs.msg import Float32
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import rospy


class PID_Controller:
    def __init__(self,gains,ref,intLimits,outLimits):
        # gains
        self.kp = gains[0]
        self.kd = gains[1]
        self.ki = gains[2]

        # reference 
        self.reference = ref
        
        # sample time in seconds
        #self.T = sampleTime 
        
        # anti wind up limits
        self.minInt = intLimits[0]
        self.maxInt = intLimits[1]
        
        # output Limits
        self.minOut = outLimits[0]
        self.maxOut = outLimits[1]

        # keep track of differnce equation time shift 
        self.prevError = 0
        self.prevMeasurement = 0
        self.integrator = 0

    def pidUpdate(self,measurement):
        error = self.reference - measurement
        proportional = self.kp * error
        self.integrator = self.integrator + self.ki  *(error - self.prevError)
        derivative = self.kd * (error - self.prevError)
        # ANTI WIND UP CLAMPING METHID 
        if(self.integrator > self.maxInt):
            self. integrator = self.maxInt
        elif(self.integrator < self.minInt):
            self.integrator = self.minInt



        output = proportional + self.integrator + derivative
        if output > self.maxOut:
            output = self.maxOut
        elif output < self.minOut:
            output = self.minOut

        self.prevError = error
        self.prevMeasurement = measurement

        return output


        