#!/usr/bin/env python
import click
import rospy
from geometry_msgs.msg import Twist 

pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
rospy.init_node('turtle')

while not rospy.is_shutdown():
	twist = Twist() #this expresses velocity in free space broken into its linear and angular parts.
	key_pressed = click.getchar()

	if key_pressed == '5':
		twist.linear.x = 1.5
	elif key_pressed == '1':
		twist.angular.z = 3.5
	elif key_pressed == '2':
		twist.linear.x = -0.6
	elif key_pressed == '3':
		twist.angular.z = -4.20

	pub.publish(twist)