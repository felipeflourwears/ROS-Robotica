#!/usr/bin/env python
import rospy
import actionlib
from math import atan2, pi, sqrt
from geometry_msgs.msg import Pose2D, Twist
from puzzlebot_msgs.msg import GoToPoseAction, GoToPoseFeedback, GoToPoseResult

RATE   =  10

THETA_THRESHOLD = 10.0 * pi / 180.0
DIST_THRESHOLD = 0.30

class Navigator():
    def __init__(self):
        self.pose2d = Pose2D()
        self.pose2d.x = 0.0
        self.pose2d.y = 0.0
        self.pose2d.theta = 0.0


        ##########################################################################################################
        # TODO: Setup ROS subscribers and publishers, use the callback functions defined bellow if required. 
        #       Your node must subscribe to your previously defined /pose2d named topic, to obtain the current robot's current estimated position info.
        #       YOur node must publish the desired robot's linear and agular velocities using the /cmd_vel topic.
        ##########################################################################################################

        # Your code here...
        self.susPosition =rospy.Subscriber("/Pose2d",Pose2D,self.poseCallback)
        self.pub=rospy.Publisher("/cmd_vel",Twist, queue_size=10)

        
        ##########################################################################################################

        rospy.init_node('puzzlebot_navigation')

        self.pub_rate = 0

        if rospy.has_param('/puzzlebot_controller/parameters/navigator_pub_rate'):
            self.pub_rate = rospy.get_param('/puzzlebot_controller/parameters/navigator_pub_rate')
            rospy.loginfo("Rate value loaded from parameter server, value = %s", self.pub_rate)
        else:
            self.pub_rate = RATE

        ##########################################################################################################
        # TODO: Setup the Action Server, use adequate message types for the feedback and result of the action.
        #       Use the callback functions defined bellow if required.
        ##########################################################################################################

        # Your code here...
        self.feedback = GoToPoseFeedback()
        self.result = GoToPoseResult()
        self.action = actionlib.SimpleActionServer('prueba', GoToPoseAction, self.actionCallback, False)

        ##########################################################################################################

        self.action.start()
        rospy.spin()

    def poseCallback(self, data):
        self.pose2d = data

    def actionCallback(self, goal):

        ##########################################################################################################
        # TODO: Fill the goal pose data
        ##########################################################################################################

        # Your code here...
        x_goal = goal.goal_pose2d.x
        y_goal = goal.goal_pose2d.y
        theta_goal = goal.goal_pose2d.theta

        ##########################################################################################################

        self.rate = rospy.Rate(self.pub_rate)
        success = False

        STATE = 0
        while not success:
            # If Action is canceled by other node, stop.
            if self.action.is_preempt_requested():
                self.action.set_preempted()
                success = False
                break

            cmd_vel = Twist()
            cmd_vel.linear.x = 0.0
            cmd_vel.linear.y = 0.0
            cmd_vel.linear.z = 0.0
            cmd_vel.angular.x = 0.0
            cmd_vel.angular.y = 0.0
            cmd_vel.angular.z = 0.0

            x_curr = self.pose2d.x
            y_curr = self.pose2d.y
            theta_curr = self.pose2d.theta


            ##########################################################################################################
            # TODO: Use the goal and current robot pose to modify the robot's linear and angular velocity.
            #       You shall only modify the linear.x and angular.z velocities.
            #       A State Machine oriented solution is recommended.
            #       Use the distance and theta thresholds to stop the vehicle trajectory or change between states.
            ##########################################################################################################
            kP=1
            kD=1
            thetam=atan2(y_goal-y_curr, x_goal-x_curr)
            errorAng=(thetam-theta_curr)
            errorPrevio=errorAng
            deltaError=errorAng-errorPrevio
            wAngular=kP*errorAng+kD*deltaError
           
            #Contador de pasos
            state='state1'
            controlAng=0.5
            velCon=0.5
            #Cambio de estados 
            thersholdAng1=theta_curr-0.0872665
            thersholdAng2=theta_curr+0.0872665
            thesholdPos1=sqrt(pow(2,y_goal-y_curr)+pow(2,x_goal-x_curr))
            distanciaL=0.1


            if state=='state1':
                cmd_vel.linear.x=0
                cmd_vel.angular.z=controlAng
                if thetam-thersholdAng1<=theta_curr and theta_curr<=thersholdAng2+thetam:
                    cmd_vel.linear.x=0
                    cmd_vel.angular.z=0
                    state='state2'
            if state=='state2':
                cmd_vel.linear.x=velCon
                cmd_vel.angular.z=0
                if thesholdPos1<distanciaL:
                    cmd_vel.linear.x=0
                    cmd_vel.angular.z=0
                    state='state3'
            if state=='state3':
                cmd_vel.linear.x=0
                cmd_vel.angular.z=controlAng
                if thetam-thersholdAng1<=theta_curr and theta_curr<=thersholdAng2+thetam:
                    cmd_vel.linear.x=0
                    cmd_vel.angular.z=0
                    success=True


            ##########################################################################################################

            self.pub.publish(cmd_vel)

            self.feedback.current_pose2d = self.pose2d
            self.action.publish_feedback(self.feedback)
            self.rate.sleep()

        if success:
            self.result.success = True
            self.action.set_succeeded(self.result)



if __name__ == '__main__':
    try:
        navigator = Navigator()
    except rospy.ROSInterruptException:
        pass

