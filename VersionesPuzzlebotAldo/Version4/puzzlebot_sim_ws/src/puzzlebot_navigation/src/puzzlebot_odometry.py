#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Pose2D
from math import cos, sin, pi

RATE   =  10

RADIUS =  0.05
BASE   =  0.18

class Odometry:
    def __init__(self):
        # Initialize wheel velocity variables
        self.wr = 0.0
        self.wl = 0.0


        ##########################################################################################################
        # TODO: Setup ROS subscribers and publishers, use the callback functions defined bellow if required. 
        #       Your node must publish a Pose2D message to a /pose2d named topic, with the robot's current estimated position info.
        ##########################################################################################################

        # Your code here...
        self.pose_pub =rospy.Publisher("/Pose2d",Pose2D,queue_size=10) 
        self.swl=rospy.Subscriber("/wl",Float32,self.wl_callback)
        self.swr=rospy.Subscriber("/wr",Float32,self.wr_callback)

        ##########################################################################################################

        rospy.init_node("puzzlebot_odometry")

        self.pub_rate = 0

        if rospy.has_param('/puzzlebot_navigation/parameters/odometry_pub_rate'):
            self.pub_rate = rospy.get_param('/puzzlebot_navigation/parameters/odometry_pub_rate')
            rospy.loginfo("Rate value loaded from parameter server, value = %s", self.pub_rate)
        else:
            self.pub_rate = RATE

        self.rate = rospy.Rate(self.pub_rate)

    # Main function
    def run(self):
        # Variable initializations
        position = Pose2D()
        position.theta = 0.0
        position.x = 0.0
        position.y = 0.0

        radius = 0.0
        base = 0.0

        if rospy.has_param('/puzzlebot_navigation/parameters/radius'):
            radius = rospy.get_param('/puzzlebot_navigation/parameters/radius')
            rospy.loginfo("Radius value loaded from parameter server, value = %s", radius)
        
        else:
            radius = RADIUS

        if rospy.has_param('/puzzlebot_navigation/parameters/base'):
            base = rospy.get_param('/puzzlebot_navigation/parameters/base')
            rospy.loginfo("Base value loaded from parameter server, value = %s", base)
        
        else:
            base = BASE

        current_time = rospy.get_time()
        last_time = rospy.get_time()

        # Main Loop
        while not rospy.is_shutdown():

            ##########################################################################################################
            # TODO: Calculate current robot position estimation, use atan2 angle convention for the orientation angle.
            ##########################################################################################################
    
            last_time=current_time
            current_time=rospy.get_time()
            dt=current_time-last_time

            #position = Pose2D()
            #position.theta = 0.0
            #position.x = 0.0
            #position.y = 0.0
            #radius = 0.0
            #base = 0.0
            position.theta=position.theta+radius*((self.wr-self.wl)/base)*dt
            position.x=position.x+radius*((self.wr+self.wl)/2)*cos(position.theta)*dt
            position.y=position.y+radius*((self.wr+self.wl)/2)*sin(position.theta)*dt

            if position.theta>pi:
                position.theta-=2*pi
            elif position.theta<-pi:
                position.theta+=2*pi
            
            #print(self.wl)
            #print(self.wr)
            #print(position.x)
            #print(position.y)
            #print(position.theta)
            ##########################################################################################################

            # Publish message and sleep
            rospy.loginfo(position)
            self.pose_pub.publish(position)
            self.rate.sleep()

    # Callbacks for wheel velocities and commands
    def wr_callback(self, msg):
        self.wr = msg.data

    def wl_callback(self, msg):
        self.wl = msg.data

if __name__ == "__main__":
    odometry = Odometry()
    try:
        odometry.run()
    except rospy.ROSInterruptException:
        pass