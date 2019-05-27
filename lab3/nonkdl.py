import json
import rospy
import os
from sensor_msgs.msg import JointState
from tf.transformations import *
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped



def callback(data):
    
    main_matrix = translation_matrix((0, 0, 0));
    x_axis, y_axis, z_axis = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    
    i=0
    for piece in dh_file:
        one_piece= json.loads(json.dumps(piece))
        a = one_piece["a"]
        d = one_piece["d"]
        al = one_piece["al"]
        th = one_piece["th"]

        matrix_d= translation_matrix((0, 0, d*(1+data.position[i])))
        matrix_th = rotation_matrix(th, z_axis)
        matrix_a = translation_matrix((a, 0, 0))
        matrix_al = rotation_matrix(al, x_axis)

        trans_matrix = concatenate_matrices(matrix_a,matrix_al,matrix_th, matrix_d)
        main_matrix = concatenate_matrices(main_matrix, trans_matrix)
        i += 1
        
    
    x, y, z = translation_from_matrix(main_matrix)
    qx, qy, qz, qw = quaternion_from_matrix(main_matrix)
    non_kdl_pose = PoseStamped()
    non_kdl_pose.header.frame_id = 'base_link'
    non_kdl_pose.header.stamp = rospy.Time.now()
    
    non_kdl_pose.pose.position.x = x
    non_kdl_pose.pose.position.y = y
    non_kdl_pose.pose.position.z = z
    non_kdl_pose.pose.orientation.x = qx
    non_kdl_pose.pose.orientation.y = qy
    non_kdl_pose.pose.orientation.z = qz
    non_kdl_pose.pose.orientation.w = qw
    pub.publish(non_kdl_pose)
    


if __name__ == '__main__':
   
    rospy.init_node('NONKDL_DKIN', anonymous=False)
    dh_file ={}


    with open(os.path.dirname(os.path.realpath(__file__)) + '/dh_parameters.json', 'r') as file:
        dh_file= json.loads(file.read())

    pub = rospy.Publisher('NoKdlAxes', PoseStamped, queue_size=10)
    rospy.Subscriber("joint_states", JointState , callback)
    
   
    rospy.spin()