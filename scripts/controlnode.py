#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from ros_lab1.msg import TurtleControl

# Global variables are used to store the value of the nodes information
current_position = None
desired_position = 0.0
control_gain = 0.0


# The following functions grabs the gloabal variables and updates the data accordingly
def pose_callback(data):
    global current_position
    current_position = data.x

def control_params_callback(data):
    global desired_position, control_gain
    desired_position = data.xd  
    control_gain = data.kp

def proportional_controller():
    global current_position, desired_position, control_gain

    # Initialize the node
    rospy.init_node('controlnode', anonymous=True)

    # Subscriber to the turtle's pose
    rospy.Subscriber("/turtle1/pose", Pose, pose_callback)

    # Subscriber to the control parameters
    rospy.Subscriber("/turtle1/control_params", TurtleControl, control_params_callback)

    # Publisher to the turtle's velocity command
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10)  # Set the loop to 10 Hz

    while not rospy.is_shutdown():
        if current_position is not None:  # Ensure current_position is not None
            # Calculate the position error
            error = desired_position - current_position

            # Proportional control law: v = Kp * error
            vel_cmd = Twist()
            vel_cmd.linear.x = control_gain * error
            vel_cmd.angular.z = 0.0

            # Publish the velocity command
            pub.publish(vel_cmd)

        rate.sleep()


