#!/usr/bin/env python
import rospy
import actionlib
from math import atan2, pi, sqrt
from geometry_msgs.msg import Pose2D, Twist
from puzzlebot_msgs.msg import GoToPoseAction, GoToPoseFeedback, GoToPoseResult, GoToPoseGoal

RATE   =  10

THETA_THRESHOLD = 10.0 * pi / 180.0
BETA_THRESHOLD = 10.0 * pi / 180.0
DIST_THRESHOLD = 0.30
kd = 0.6
kp = 0.4

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
        self.pose2d = rospy.Subscriber('/Pose2d', Pose2D, self.poseCallback)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)

        ##########################################################################################################

        rospy.init_node('puzzlebot_navigation')

        self.pub_rate = 0

        if rospy.has_param('/puzzlebot_navigation/parameters/navigator_pub_rate'):
            self.pub_rate = rospy.get_param('/puzzlebot_navigation/parameters/navigator_pub_rate')
            rospy.loginfo("Rate value loaded from parameter server, value = %s", self.pub_rate)
        else:
            self.pub_rate = RATE

        self.theta_threshold = 0

        if rospy.has_param('/puzzlebot_navigation/parameters/theta_threshold'):
            self.theta_threshold = rospy.get_param('/puzzlebot_navigation/parameters/theta_threshold')
            rospy.loginfo("Rate value loaded from parameter server, value = %s", self.theta_threshold)
        else:
            self.theta_threshold = THETA_THRESHOLD

        self.beta_t = 0

        if rospy.has_param('/puzzlebot_navigation/parameters/beta_threshold'):
            self.beta_t = rospy.get_param('/puzzlebot_navigation/parameters/beta_threshold')
            rospy.loginfo("Rate value loaded from parameter server, value = %s", self.beta_t)
        else:
            self.beta_t = BETA_THRESHOLD

        self.dist_t = 0

        if rospy.has_param('/puzzlebot_navigation/parameters/dist_threshold'):
            self.dist_t = rospy.get_param('/puzzlebot_navigation/parameters/dist_threshold')
            rospy.loginfo("Rate value loaded from parameter server, value = %s", self.dist_t)
        else:
            self.dist_t = DIST_THRESHOLD



        ##########################################################################################################
        # TODO: Setup the Action Server, use adequate message types for the feedback and result of the action.
        #       Use the callback functions defined bellow if required.
        ##########################################################################################################

        # Your code here...
        self.feedback = GoToPoseFeedback()
        self.result = GoToPoseResult()
        self.action = actionlib.SimpleActionServer('prueba', GoToPoseAction, execute_cb= self.actionCallback)

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

        cmd_vel = Twist()
        cmd_vel.linear.x = 0.0
        cmd_vel.linear.y = 0.0
        cmd_vel.linear.z = 0.0
        cmd_vel.angular.x = 0.0
        cmd_vel.angular.y = 0.0
        cmd_vel.angular.z = 0.0

        delta_beta = 0.0
        delta_d = 0.0
        delta_theta = 0.0

        current_time = rospy.get_time()
        last_time = current_time

        while not success:
            # If Action is canceled by other node, stop.
            if self.action.is_preempt_requested():
                self.action.set_preempted()
                success = False
                break

            x_curr = self.pose2d.x
            y_curr = self.pose2d.y
            theta_curr = self.pose2d.theta


            ##########################################################################################################
            # TODO: Use the goal and current robot pose to modify the robot's linear and angular velocity.
            #       You shall only modify the linear.x and angular.z velocities.
            #       A State Machine oriented solution is recommended.
            #       Use the distance and theta thresholds to stop the vehicle trajectory or change between states.
            ##########################################################################################################

            # Your code here...

            desired_angle = atan2(y_goal-y_curr, x_goal-x_curr) 

            delta_theta_p = delta_theta
            delta_beta_p = delta_beta

            delta_theta = desired_angle - theta_curr
            delta_beta = theta_goal - theta_curr

            if (delta_theta > pi):
                delta_theta = delta_theta - 2*pi
            elif (delta_theta < -pi):
                delta_theta = delta_theta + 2*pi

            if (delta_beta > pi):
                delta_beta = delta_theta - 2*pi
            elif (delta_beta < -pi):
                delta_beta = delta_theta + 2*pi

            rospy.loginfo(delta_theta)
            rospy.loginfo(delta_beta)

            current_time = rospy.get_time()

            dt = current_time - last_time

            if (dt == 0):
                dt = 0.001

            last_time = current_time

            if STATE == 0:   

                if (abs(delta_theta) < self.theta_threshold):
                    cmd_vel.linear.x = 0.0
                    cmd_vel.angular.z = 0.0
                    STATE = 1
                else:
                    cmd_vel.linear.x = 0.0
                    cmd_vel.angular.z = kp*delta_theta + kd * (delta_theta - delta_theta_p)/ dt
                    STATE = 0
            
            elif STATE == 1:

                delta_d = abs(sqrt(((x_goal-x_curr)**2)+((y_goal-y_curr)**2))) 

                if (delta_d < self.dist_t):
                    cmd_vel.linear.x = 0.0
                    cmd_vel.angular.z = 0.0
                    STATE = 2

                else:
                    cmd_vel.linear.x = 0.1
                    cmd_vel.angular.z = kp*delta_theta + kd * (delta_theta - delta_theta_p)/ dt
                    STATE = 1

            elif STATE == 2:

                if (abs(delta_beta) < self.beta_t):
                    cmd_vel.angular.z = 0.0
                    cmd_vel.linear.x = 0.0
                    STATE = 3
                else:
                    cmd_vel.linear.x = 0.0
                    cmd_vel.angular.z = 0.5*delta_beta + kd * (delta_beta - delta_beta_p)/ dt
                    STATE = 2
            else:
                success = True

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