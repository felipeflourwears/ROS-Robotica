#! /usr/bin/env python
from ast import While
from calendar import c
import rospy
from geometry_msgs.msg import Twist
import sys


#Ver el publisher rostopic list
#/turtle1/cmd_vel

def move_turtle():
    #rospy.init_node('turtlemove',anonymous=True)
    rospy.init_node('turtlemove')
    pub=rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
    rate=rospy.Rate(10)
    vel=Twist()


    #Contador de pasos
    count=0
    #Cambio de estados 
    # R-->Rotation
    # F-->Forward
    state='forward'
    
    
    #Ver los parametros en la terminal rostopic pub /turtle1/cmd_vel geoist "linear:wi


    while not rospy.is_shutdown():
        
        #Velocidad lineal
        vel.linear.x=0
        vel.linear.y=0
        vel.linear.z=0
        #Velocidad angular
        vel.angular.x=0
        vel.angular.y=0
        vel.angular.z=0
        
        if state=='forward' and count>=10:
            state='rotation'
            count=0
        if state=='rotation' and count>=16:
            count=0
            state='forward'
        if state=='forward' and count<20:
            vel.linear.x=1
            vel.angular.z=0
        if state=='rotation' and count<20:
            vel.linear.x=0
            vel.angular.z=1
        
        print(count)
        count=count+1
        #print(count)
        print(state)
        #count=count+1  
        pub.publish(vel)
        rate.sleep()
if __name__ == "__main__":
    move_turtle()

    #rosrun turtlesim turtlesim_node 
"""
Estrella: 25,25,25,25
Pentagono 25,50,25,50
Triangulo 10,20,10,20
Cuadrado deforme 10,15,20,20
"""