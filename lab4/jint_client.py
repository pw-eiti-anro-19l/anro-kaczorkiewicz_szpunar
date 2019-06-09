import sys
import rospy
from lab4.srv import *
from lab4.msg import *

def jint_control_srv_client(x, y):
    rospy.wait_for_service('jint_control_srv')
    try:
        add_two_ints = rospy.ServiceProxy('jint_control_srv', JintControlSrv)
        resp1 = add_two_ints(x, y)
        return resp1.sum
    except rospy.ServiceException:
        print("Service call failed")

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print(usage())
        sys.exit(1)
    print("Requesting %s+%s"%(x, y))
    print("%s + %s = %s"%(x, y, jint_control_srv_client(x, y)))