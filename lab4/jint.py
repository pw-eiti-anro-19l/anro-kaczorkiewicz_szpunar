import rospy
from lab4.srv import *
from lab4.msg import *



def handle_jint_control_srv(req):
    print("handle arg: [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
    return JintControlSrvResponse(req.a - req.b)

if __name__ == '__main__':
    
    rospy.init_node('jint', anonymous=False)
    service = rospy.Service('jint_control_srv', JintControlSrv, handle_jint_control_srv)
    print("lol")
    
    rospy.spin()