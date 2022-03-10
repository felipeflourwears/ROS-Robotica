#! /usr/bin/env python
from ast import While
import rospy
from geometry_msgs.msg import Twist
import sys

#Ver el publisher rostopic list
#/turtle1/cmd_vel

def move_turtle(line_vel,ang_vel):
    #rospy.init_node('turtlemove',anonymous=True)
    rospy.init_node('turtlemove')
    pub=rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
    rate=rospy.Rate(10)
    vel=Twist()
    #Ver los parametros en la terminal rostopic pub /turtle1/cmd_vel geoist "linear:wi
    while not rospy.is_shutdown():
        #Velocidad lineal
        vel.linear.x=line_vel
        vel.linear.y=0
        vel.linear.z=0

        #Velocidad angular
        vel.angular.x=0
        vel.angular.y=0
        vel.angular.z=ang_vel

        pub.publish(vel)
        rate.sleep()
if __name__ == "__main__":
    move_turtle(3.0,2.5)
    #rosrun turtlesim turtlesim_node 
