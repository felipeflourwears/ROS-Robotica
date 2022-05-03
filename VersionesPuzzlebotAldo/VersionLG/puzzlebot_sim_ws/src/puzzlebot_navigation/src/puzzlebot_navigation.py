#!/usr/bin/env python
import rospy
import actionlib
from math import atan2, pi, sqrt
from geometry_msgs.msg import Pose2D, Twist
from puzzlebot_msgs.msg import GoToPoseAction, GoToPoseFeedback, GoToPoseResult

RATE   =  10

THETA_THRESHOLD = 10.0 * pi / 180.0
DIST_THRESHOLD = 0.3

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
        current_time=rospy.get_time()
        last_time=rospy.get_time()
        theta_err2_p=0
        theta_err_p=0


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
            current_time=rospy.get_time()
            dt=current_time-last_time
            last_time=current_time
            #Controlador
            kp=0.60
            kd=0.4
          

            theta_obj=atan2(y_goal-y_curr, x_goal-x_curr)
            theta_err=theta_obj-theta_curr
            if theta_err>=pi:
                theta_err-=2*pi
            elif theta_err<=-pi:
                theta_err+=2*pi
            theta_err2=theta_goal-theta_curr
            
            if theta_err2>=pi:
                theta_err2-=2*pi
            elif theta_err2<=-pi:
                theta_err2+=2*pi
            rospy.loginfo(theta_err)
            rospy.loginfo(theta_err2)


            dist_err = sqrt((y_goal-y_curr)** 2 + (x_goal-x_curr)** 2)

            if STATE == 0:
                if dt==0: dt=0.00001
                cmd_vel.angular.z=(kp*theta_err)+(kd*((theta_err-theta_err_p)/dt))
                if cmd_vel.angular.z >= 0.75:
                    cmd_vel.angular.z = 0.75
                elif cmd_vel.angular.z <= -0.75:
                    cmd_vel.angular.z= -0.75
                cmd_vel.linear.x=0
                theta_err_p=theta_err
                if abs(theta_err)<THETA_THRESHOLD:    
                    STATE += 1
            elif STATE == 1:
                cmd_vel.angular.z=(kp*theta_err)+(kd*((theta_err-theta_err_p)/dt))
                if cmd_vel.angular.z >= 0.75:
                    cmd_vel.angular.z =  0.75
                elif cmd_vel.angular.z <= -0.75:
                    cmd_vel.angular.z= -0.75
                cmd_vel.linear.x=0.35
                theta_err_p=theta_err
                if dist_err <= DIST_THRESHOLD:
                    STATE += 1
            elif STATE == 2:
                if dt==0: dt=0.00001
                cmd_vel.angular.z = (kp * theta_err2) + (kd * ((theta_err2-theta_err2_p)/dt))
                if cmd_vel.angular.z >= 0.75:
                    cmd_vel.angular.z = 0.75
                elif cmd_vel.angular.z <= -0.75:
                    cmd_vel.angular.z = -0.75
                cmd_vel.linear.x=0
                theta_err2_p = theta_err2

                if abs(theta_err2)<THETA_THRESHOLD:
                    STATE+=1
            else:
                cmd_vel.angular.z = 0
                cmd_vel.linear.x = 0
                success=True
                print(success)


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