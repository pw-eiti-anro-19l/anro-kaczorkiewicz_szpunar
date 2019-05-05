import rospy
import json
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker

def callback(data):
    main_matrix = translation_matrix((0, 0, 0))

    counter = 0
    for i in json_file:
        print(data)
        params = json.loads(json.dumps(i))
        a = params["a"]
        d = params["d"]
        al = params["al"]
        th = params["th"]

        matrix_a = translation_matrix((a, 0, 0))
        matrix_al = rotation_matrix(al, (1, 0, 0))
        matrix_d= translation_matrix((0, 0, d*(1+data.position[counter])))
        matrix_th = rotation_matrix(th, (0, 0, 1))

        trans = concatenate_matrices(matrix_a, matrix_al, matrix_d, matrix_th)
        t_list[counter] = trans

        counter += 1

    main_matrix = concatenate_matrices(t_list[0], t_list[1], t_list[2])

    x, y, z = translation_from_matrix(main_matrix)
    
    robot_pose = PoseStamped()
    robot_pose.header.frame_id = "base_link"
    robot_pose.header.stamp = rospy.Time.now()
    robot_pose.pose.position.x = x
    robot_pose.pose.position.y = y
    robot_pose.pose.position.z = z
    
    xq, yq, zq, wq = quaternion_from_matrix(main_matrix)

    robot_pose.pose.orientation.x = xq
    robot_pose.pose.orientation.y = yq
    robot_pose.pose.orientation.z = zq
    robot_pose.pose.orientation.w = wq

    publisher.publish(robot_pose)

def nonkdl_listener():
    rospy.init_node('NONKDL_DKIN', anonymous = False)
    # publisher = rospy.Publisher('n_k_axes', PoseStamped, queue_size=10)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':
    json_file = {}
    t_list = {}
    publisher = rospy.Publisher('n_k_axes', PoseStamped, queue_size=10)

    with open('dh_parameters.json', 'r') as file:
        json_file = json.loads(file.read())
    
    # laczenie z modelem
    try:
	    nonkdl_listener()        
    except rospy.ROSInterruptException:
        pass
