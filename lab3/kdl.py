import json
import rospy
import PyKDL
import os
from sensor_msgs.msg import JointState
from tf.transformations import *
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped


def callback(data):

    kdl_chain =PyKDL.Chain()   
    Frame = PyKDL.Frame();

    d=0
    th=0
    i=1
    for piece in dh_file:
        one_piece= json.loads(json.dumps(piece))
        last_d = d
        last_th = th
        a = one_piece["a"]
        d = one_piece["d"]
        al=one_piece["al"]
        th = one_piece["th"]
        if i!= 1:
            kdl_chain.addSegment(PyKDL.Segment(PyKDL.Joint(PyKDL.Joint.TransZ), Frame.DH(a, al, last_d, last_th)))
        i += 1
    kdl_chain.addSegment(PyKDL.Segment(PyKDL.Joint(PyKDL.Joint.TransZ), Frame.DH(0, 0, d, th)))
      
      
    jointDisplacement = PyKDL.JntArray(kdl_chain.getNrOfJoints())

    jointDisplacement[0] = data.position[0]
    jointDisplacement[1] = data.position[1]
    jointDisplacement[2] = data.position[2]

    f_k_solver = PyKDL.ChainFkSolverPos_recursive(kdl_chain)

    frame = PyKDL.Frame()
    f_k_solver.JntToCart(jointDisplacement, frame)
    quatr = frame.M.GetQuaternion()
    
    kdl_pose = PoseStamped()
    kdl_pose.header.frame_id = 'base_link'
    kdl_pose.header.stamp = rospy.Time.now()

    kdl_pose.pose.position.x = frame.p[0]
    kdl_pose.pose.position.y = frame.p[1]
    kdl_pose.pose.position.z = frame.p[2]
    kdl_pose.pose.orientation.x = quatr[0]
    kdl_pose.pose.orientation.y = quatr[1]
    kdl_pose.pose.orientation.z = quatr[2]
    kdl_pose.pose.orientation.w = quatr[3]
    pub.publish(kdl_pose)
    


if __name__ == '__main__':
    
    rospy.init_node('KDL_DKIN', anonymous=False)
    dh_file ={}
       
    with open(os.path.dirname(os.path.realpath(__file__)) + '/dh_parameters.json', 'r') as file:
        dh_file= json.loads(file.read())

    pub = rospy.Publisher('k_axes', PoseStamped, queue_size=10)
    rospy.Subscriber("joint_states", JointState , callback)
    
   
    rospy.spin()