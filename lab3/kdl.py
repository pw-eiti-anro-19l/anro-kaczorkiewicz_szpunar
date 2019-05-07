import rospy
import json
import PyKDL as kdl
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker


def callback(data):
    kdlChain =kdl.Chain()   
    frame = kdl.Frame();
    main_matrix = translation_matrix((0, 0, 0))
    d=0
    th=0
    counter = 0
    for i in json_file:
        #print(data)
        params = json.loads(json.dumps(i))

        last_d = d
        last_th = th
        a = params["a"]
        d = params["d"]
        al = params["al"]
        th = params["th"]

        if counter!= 0:
        	kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), frame.DH(a - 0.5, al, d - 0.5, th)))

        counter += 1
    		
    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), frame.DH(0, 0, d, th)))
    	

    jointPos = kdl.JntArray(kdlChain.getNrOfJoints())
    jointPos[0] = data.position[0] 
    jointPos[1] = data.position[1]
    jointPos[2] = data.position[2]
    
    forvKin = kdl.ChainFkSolverPos_recursive(kdlChain)
    eeFrame = kdl.Frame() # <--polaczyc eeFrame z reszta robota
    forvKin.JntToCart(jointPos, eeFrame)
    print(eeFrame)



    quaternion = eeFrame.M.GetQuaternion()

    
    robot_pose = PoseStamped()
    robot_pose.header.frame_id = 'base_link'
    robot_pose.header.stamp = rospy.Time.now()


    robot_pose.pose.position.x = eeFrame.p[0]
    robot_pose.pose.position.y = eeFrame.p[1]
    robot_pose.pose.position.z = eeFrame.p[2]

    robot_pose.pose.orientation.x = quaternion[0]
    robot_pose.pose.orientation.y = quaternion[1]
    robot_pose.pose.orientation.z = quaternion[2]
    robot_pose.pose.orientation.w = quaternion[3]
    publisher.publish(robot_pose)

def kdl_listener():
    rospy.init_node('KDL_DKIN', anonymous = False)
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
	    kdl_listener()        
    except rospy.ROSInterruptException:
        pass
