import json
import rospy
import os
from sensor_msgs.msg import JointState
from tf.transformations import *
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped


def is_positive(data):
    i=0
    for piece in restrictions_file:
        one_piece= json.loads(json.dumps(piece))
        if data.position[i]>one_piece["forward"] or data.position[i]<one_piece["backward"] :
            return False
        i=i+1
    return True
def callback(data):
    if is_positive(data)==False:
        rospy.logerr("Position is not available: " + str(data))
        return
    main_matrix = translation_matrix((0, 0, 0));
    
    i=0
    for piece in dh_file:
        one_piece= json.loads(json.dumps(piece))
        a = one_piece["a"]
        d = one_piece["d"]
        al = one_piece["al"]
        th = one_piece["th"]

        matrix_d= translation_matrix((0, 0, d*(1+data.position[i])))
        matrix_th = rotation_matrix(th, zaxis)
        matrix_a = translation_matrix((a, 0, 0))
        matrix_al = rotation_matrix(al, xaxis)

        trans_matrix = concatenate_matrices(matrix_a,matrix_al,matrix_th, matrix_d)
        main_matrix = concatenate_matrices(main_matrix, trans_matrix)
        i += 1
        
    
    x, y, z = translation_from_matrix(main_matrix)
    qx, qy, qz, qw = quaternion_from_matrix(main_matrix)
    kdl_pose = PoseStamped()
    kdl_pose.header.frame_id = 'base_link'
    kdl_pose.header.stamp = rospy.Time.now()
    
    kdl_pose.pose.position.x = x
    kdl_pose.pose.position.y = y
    kdl_pose.pose.position.z = z
    kdl_pose.pose.orientation.x = qx
    kdl_pose.pose.orientation.y = qy
    kdl_pose.pose.orientation.z = qz
    kdl_pose.pose.orientation.w = qw
    pub.publish(kdl_pose)
    


if __name__ == '__main__':
    xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    rospy.init_node('NONKDL_DKIN', anonymous=False)
    dh_file ={}
    restrictions_file ={}
    with open(os.path.dirname(os.path.realpath(__file__)) + '/restrictions.json', 'r') as file:
        restrictions_file= json.loads(file.read())
   
    with open(os.path.dirname(os.path.realpath(__file__)) + '/dh_parameters.json', 'r') as file:
        dh_file= json.loads(file.read())

    pub = rospy.Publisher('NoKdlAxes', PoseStamped, queue_size=10)
    rospy.Subscriber("joint_states", JointState , callback)
    
   
    rospy.spin()