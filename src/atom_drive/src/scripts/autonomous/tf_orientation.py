#!/usr/bin/env python

#this is a simple program that subscribes to the odom topic and gets the position and orientation of the robot
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Quaternion
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
import math
import time
from std_srvs.srv import Empty
import tf

#callback function the odom pose (position+orientation) of the robot 
def IMUCallback(imu_msg):

    #print ("IMU callback")
    # #get the position of the robot
    # print ('x = ',imu_msg.pose.pose.position.x)
    # print ('y = ', imu_msg.pose.pose.position.y) 
    # #get the velocity of the robot
    # print ('vx = ',imu_msg.twist.twist.linear.x)
    # print ('vz = ',imu_msg.twist.twist.angular.z)

    #print the values of the orientation in quaternion
    # print ('qx=',imu_msg.orientation.x)
    # print ('qy=',imu_msg.orientation.y)
    # print ('qz=',imu_msg.orientation.z)
    # print ('qw=',imu_msg.orientation.w)
    
    #formulate a quaternion as a list
    quaternion = (
    imu_msg.orientation.x,
    imu_msg.orientation.y,
    imu_msg.orientation.z,
    imu_msg.orientation.w)
    
    #convert the quaternion to roll-pitch-yaw
    rpy = tf.transformations.euler_from_quaternion(quaternion)
    #extract the values of roll, pitch and yaw from the array
    roll = rpy[0]
    pitch = rpy[1]
    yaw = rpy[2]

    #print the roll, pitch and yaw
    #rospy.loginfo('The orientation of the robot is: %f',math.degrees(yaw))
    
    
    # print (math.degrees(roll), ' ', math.degrees(pitch), ' ', math.degrees(yaw))
    print ('The orientation of the robot is: ',math.degrees(yaw))
 


if __name__ == '__main__':
    try:
        #init the node
        rospy.init_node('turtlesim_motion_pose', anonymous=True)
       
       #subscribe to the odom topic 
        position_topic = "/phone1/android/imu"
        pose_subscriber = rospy.Subscriber(position_topic, Imu, IMUCallback) 
        #spin
        rospy.spin()
       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
