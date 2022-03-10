#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
if __name__ == "__main__":
    publisher = rospy.Publisher("chatter",String,queue_size=10) # construir un objeto publisherlisher
    rospy.init_node("talker")
    rate = rospy.Rate(10) # manda un mensaje a una frequencia de 10Hz
    while not rospy.is_shutdown(): # mientras el nodo este activo...
        msg = "Hello world %s" % rospy.get_time() # crear un mensaje que manda el tiempo
        publisher.publish(msg) # publisherlicar cuando se manda el mensaje a los subscriptores
        rate.sleep() # duermete por 10HZ (asi se definió)



#     while not rospy.is_shutdown: # mientras el nodo este activo...
