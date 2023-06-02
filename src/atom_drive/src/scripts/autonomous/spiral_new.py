#! /usr/bin/env python

import rospy
from atom_drive.msg import Drive
# from atom_drive.msg import Arrow
import tf
import numpy as np
from sensor_msgs.msg import Imu
import math
x=0
y=0

time=0
def subscriber(initial):

    rospy.Subscriber('/phone1/android/imu', Imu, callback,callback2(initial))

def callback(data):

    global x 
    global y
    global time

    quaternion = (data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)
    rpy = tf.transformations.euler_from_quaternion(quaternion)
    yaw2 = rpy[2]
    yaw = math.degrees(yaw2)
    x = yaw
    time = rospy.get_time() - initial
    # y = data.boolean
    rospy.loginfo(time)


def callback2(initial):
    global time
    time=rospy.get_time() - initial

def turn(pub,core,rate,yaw):
    global x 
    while abs(x - yaw) < 90:

        core.ld = 2
        core.ls = 150
        core.rd = 1
        core.rs = 150

        pub.publish(core)
        rate.sleep()       

count = 1
turn_time = 8
def publisher(pub):
    global x 
    global count
    global interval
    global turn_time
    global time
    rospy.loginfo('connected')
    core = Drive()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        if y == 0 :

            if abs(time - turn_time) < 0.02:
                interval = (count+1)*8
                turn_time = turn_time + interval + 3*(count)
                count = count + 1
                turn(pub,core,rate,x)

            else :
                core.ld = 2
                core.ls = 150
                core.rd = 2
                core.rs = 150

                pub.publish(core)
                rate.sleep()                





if __name__ == "__main__":
    pub = rospy.Publisher('spiral/move',Drive,queue_size = 20)
    rospy.init_node('spiral_move',anonymous=True)
    initial=rospy.get_time()
    subscriber(initial)
    publisher(pub)


 








# #! usr/bin/env python

# import rospy
# from atom_drive.msg import Drive
# from atom_drive.msg import Arrow
# import tf
# import numpy as np
# from sensor_msgs.msg import Imu
# import math

# def subscriber():
#     rospy.init_node('spiral_move',anonymous=True)
#     rospy.Subscriber('arrow/detect', Arrow, callback)

# def callback(data):

#     global x 
#     global y

#     quaternion = (data.data.orientation.x, data.data.orientation.y, data.data.orientation.z, data.data.orientation.w)
#     rpy = tf.transformations.euler_from_quaternion(quaternion)
#     yaw2 = rpy[2]
#     yaw = math.degrees(yaw2)
#     x = yaw
#     time = rospy.get_time()
#     y = data.boolean

# def turn(pub,core,rate,yaw):
#     global x 
#     while abs(x - yaw) < 90:

#         core.ld = 2
#         core.ls = 150
#         core.rd = 1
#         core.rs = 150

#         pub.publish(core)
#         rate.sleep()       

# count = 1
# turn_time = 15
# def publisher(pub):
#     global x 
#     global count
#     global interval
#     global turn_time
#     rospy.loginfo('connected')
#     core = Drive()
#     rate = rospy.Rate(10)

#     if y == 0 :
#         while not rospy.is_shutdown():
#             if time - turn_time < 2:
#                 interval = (count+1)*10
#                 turn_time = turn_time + interval + 23*(count)
#                 count = count + 1
#                 turn(pub,core,rate,x)

#             else :
#                 core.ld = 2
#                 core.ls = 150
#                 core.rd = 2
#                 core.rs = 150

#                 pub.publish(core)
#                 rate.sleep()                





# if __name__ == "__main__":
#     pub = rospy.Publisher('spiral/move',Drive,queue_size = 20)

#     subscriber()
#     publisher(pub)


 
