#! /usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

#def pose_callback(msg: Pose):
 #   rospy.loginfo(str(msg.x))

 
def call_set_pen_service(r, g, b, width, off):
    try:
        set_pen = rospy.ServiceProxy("/turtle1/set_pen", SetPen)
        response = set_pen(r,g,b,width,off)
        
    except rospy.ServiceException as e:
        pass


if __name__ == '__main__':
    rospy.init_node("spiral")
    rospy.loginfo("Drawing Spiral")

    rospy.wait_for_service("/turtle1/set_pen")

    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = 10)
    #sub = rospy.Subscriber("/turtle1/pose", Pose, callback = pose_callback)
    rate = rospy.Rate(0.01)

    speed = 0.1
    r = 254
    g = 0
    b = 1
    call_set_pen_service(255,0,0,4,0)


    while not rospy.is_shutdown():
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = 1.0
        speed += 0.001
        pub.publish(msg)
        if (r != 0 and b != 0) or b == 255 :
           r += 1
           b -= 1
        elif r == 255 or (r != 0 and g != 0):
           r -= 1
           g += 1
        elif g == 255 or (g != 0 and b != 0):
           g -= 1
           b += 1

        call_set_pen_service(r,g,b,4,0)


        rate.sleep