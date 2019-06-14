#!/usr/bin/env python
 
import rospy
from lab4.srv import Jint
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math
import os
import json
from sensor_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped
 

freq = 50
start = [ 0, 0, 0] 

def interpolate(jMsg):
	global start
	if (jMsg.j1>1 or jMsg.j2>1 or jMsg.j3>1):
		return ("bawi cie to?")
 
	end = [jMsg.j1, jMsg.j2, jMsg.j3]
 	
 	change = start
	step=[(end[0]-start[0])/(freq*jMsg.time),(end[1]-start[1])/(freq*jMsg.time),(end[2]-start[2])/(freq*jMsg.time)]
	for k in range(0, int(freq*jMsg.time)+1):
		for i in range(0, 3):
			change[i]=change[i]+step[i]
		start=[change[0],change[1],change[2]]
  
		robot_pose = PoseStamped()
		robot_pose.header.frame_id = "base_link"
        	robot_pose.header.stamp = rospy.Time.now()
        	robot_pose.pose.position.x = change[0]
        	robot_pose.pose.position.y = change[1]
        	robot_pose.pose.position.z = change[2]
   
		rate = rospy.Rate(50) # 50hz
        	pub.publish(robot_pose)
        	rate.sleep()
 
	current_time = 0
	start = end
	return (str(jMsg.j1)+" "+str(jMsg.j2)+" "+str(jMsg.j3))

 
 
if __name__ == "__main__":
	rospy.init_node('int_srv')
	pub = rospy.Publisher('oint',PoseStamped, queue_size=10)
	s = rospy.Service('ointApp', Jint, interpolate)
	rospy.spin()
