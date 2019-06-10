#!/usr/bin/env python

import rospy
from lab2.srv import Jint
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math


freq = 50
flag = 0

start = [0, 0, 0]
def interpolate(jMsg):
    if(jMsg.j1>1 or jMsg.j2>1 or jMsg.j3>1):
        return ("Przestan smieszku z nami tak poigrywac")
    global start
    end = [jMsg.j1, jMsg.j2, jMsg.j3]
    change = start
    step=[(end[0]-start[0])/(freq*jMsg.time),(end[1]-start[1])/(freq*jMsg.time),(end[2]-start[2])/(freq*jMsg.time)]
    for k in range(0, int(freq*jMsg.time)+1):
	for i in range(0, 3):
	    change[i]=change[i]+step[i]
	    
	    rate = rospy.Rate(50) 
        pose_str = JointState()
        pose_str.header.stamp = rospy.Time.now()
        pose_str.name = ['base_to_link1', 'link1_to_link2', 'link2_to_link3'] #wskazanie jointow
        pose_str.position = [change[0], change[1], change[2]] #ruch jointow
        pub.publish(pose_str)
        rate.sleep()


    current_time = 0
    start = end
    return (str(jMsg.j1)+" "+str(jMsg.j2)+" "+str(jMsg.j3))


if __name__ == "__main__":

    rospy.init_node('int_srv')
    pub = rospy.Publisher('joint_states',JointState,queue_size=10)
    s = rospy.Service('jintApp', Jint, interpolate)
    rospy.spin()
