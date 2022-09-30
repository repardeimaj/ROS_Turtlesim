#! /usr/bin/env python3
import tarfile
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from turtlesim.srv import Spawn    
import math


class catcher:
    target_x = float(0)
    target_y = float(0)

    current_x = float(0)
    current_y = float(0)
    current_angle = float

    pub = rospy.Publisher

    def __init__(self):
        rospy.init_node("chaser")
        rospy.loginfo("Chase Turtle")

        rospy.wait_for_service("/spawn")
        self.spawn("turtle2",0,0)

        self.pub = rospy.Publisher("/turtle2/cmd_vel", Twist, queue_size = 10)
        sub = rospy.Subscriber("/turtle1/pose", Pose, callback = self.target_pose_callback)
        sub2 = rospy.Subscriber("/turtle2/pose", Pose, callback = self.my_pose_callback)

        
        rate = rospy.Rate(50)


        rospy.wait_for_service("/turtle1/set_pen")
        self.call_set_pen_service(0,255,0,4,0)

        while not rospy.is_shutdown():
            dx = float(self.target_x - self.current_x)
            dy = float(self.target_y - self.current_y)

            kp = 1
            
            
            error_theta = float(0.0)
            if math.sqrt(dx*dx + dy*dy) != 0.0:
                error_theta = float(math.acos((dx) / math.sqrt(dx * dx + dy * dy) * float(math.cos(self.current_angle)) +  (dy) / math.sqrt(dx * dx + dy * dy) * math.sin(self.current_angle)))
                if float((dy) /math.sqrt(dx * dx + dy * dy) * math.cos(self.current_angle) - (dx) / math.sqrt(dx * dx + dy * dy) * math.sin(self.current_angle)) < 0.0:
                    error_theta *= -1.0

                
            msg = Twist()
            msg.angular.z = kp * error_theta
            msg.linear.x = 1
            #rospy.loginfo(str(self.current_angle))

            self.pub.publish(msg)

            rate.sleep


    def my_pose_callback(self, msg: Pose):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_angle = msg.theta

    def target_pose_callback(self, msg: Pose):
        self.target_x = msg.x
        self.target_y = msg.y        
 
    def call_set_pen_service(self, r, g, b, width, off):
        try:
            set_pen = rospy.ServiceProxy("/turtle1/set_pen", SetPen)
            response = set_pen(r,g,b,width,off)
        
        except rospy.ServiceException as e:
            pass

    def spawn(self, name, x,y):
        try:
            spawner = rospy.ServiceProxy("/spawn", Spawn)
            spawner(6,2,0,"turtle2")        
        except rospy.ServiceException as e:
            rospy.loginfo("SOmething went wrong")


if __name__ == '__main__':
    x = catcher()


