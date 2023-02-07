#! /usr/bin/env python
import rospy
import cv2
import pyrealsense2
import numpy as np
import pyrealsense2 as rs
from atom_drive.msg import Middle_list   #list of two int32
from atom_drive.msg import Drive
from std_msgs.msg import Float32
from sensor_msgs.msg import Imu
import tf
import math

#a = 0
x = 0
y = 0
z = 0
val = 0

def subscriber():
    rospy.init_node('auto_calibrate',anonymous=True)
    rospy.Subscriber('forward/move',Middle_list,callback)


def subscriber2():
    rospy.Subscriber("phone1/android/imu",Imu,callback2)

def callback2(data2):
    global a
    global i
    global count
    global b

    quaternion = (data2.orientation.x, data2.orientation.y, data2.orientation.z, data2.orientation.w)
    rpy = tf.transformations.euler_from_quaternion(quaternion)
    yaw2 = rpy[2]
    yaw = math.degrees(yaw2)
    a = yaw
    # if i == 1 :
    #     b=a

    # count.append(a)

    # i=i+1

def callback(data):
    global x
    global y
    global z
    global w
    global k
    global val
    global time
    x = data.horizontal
    y = data.vertical
    z = data.distance
    w = data.detect
    k = data.direction
    time = rospy.get_time
    if data.detect == 1:
        val  = val + 1
    elif data.detect == 0:
        val = 0





def straight(pub,core,rate,yaw,t):
    global a
    global time
    while val < 15:
        #move straight for 10 secs
        #move right then left then right
    #exit

        # while (time - t) < 8:
        for i in range(0,100):
            while a - yaw > 4:
                core.ld = 2
                core.ls = 110
                core.rd = 1
                core.rs = 110
                # print(a-yaw)
                # print(a)
                # print(yaw)
                if val > 15:
                    break
                pub.publish(core)
                rate.sleep() 

            while a - yaw < -4:
                core.ld = 1
                core.ls = 110
                core.rd = 2
                core.rs = 110
                # print(a-yaw)
                # print(a)
                # print(yaw)
                if val > 15:
                    break
                pub.publish(core)
                rate.sleep() 
            core.ld = 1
            core.ls = 150
            core.rd = 1
            core.rs = 150
            rospy.loginfo("straight")
            # print(a-yaw)
            # print(a)
            # print(yaw)
            if val > 15:
                break
            pub.publish(core)
            rate.sleep()
        t = time
        yaw = a

        # while  time - t < 10:
        while abs(a - yaw) < 20:
            core.ld = 2
            core.ls = 110
            core.rd = 1
            core.rs = 110
            rospy.loginfo("first")
            # print(a-yaw)
            # print(a)
            # print(yaw)
            if val > 15:
                break
            pub.publish(core)
            rate.sleep()


        for i in range(0,20):
            core.ld = 0
            core.ls = 0
            core.rd = 0
            core.rs = 0
            rospy.loginfo("straight")
            # print(a-yaw)
            # print(a)
            # print(yaw)
            if val > 15:
                break
            pub.publish(core)
            rate.sleep()
        yaw = a
        while abs(a - yaw) < 40:
            core.ld = 1
            core.ls = 110
            core.rd = 2
            core.rs = 110
            rospy.loginfo("second")
            # print(a-yaw)
            # print(a)
            # print(yaw)

            if val > 15:
                break

            pub.publish(core)
            rate.sleep()

        for i in range(0,20):
            core.ld = 0
            core.ls = 0
            core.rd = 0
            core.rs = 0
            rospy.loginfo("straight")
            # print(a-yaw)
            # print(a)
            # print(yaw)
            if val > 15:
                break
            pub.publish(core)
            rate.sleep()

        yaw = a

        while abs(a - yaw) < 21:
            core.ld = 2
            core.ls = 110
            core.rd = 1
            core.rs = 110
            rospy.loginfo("third")
            # print(a-yaw)
            # print(a)
            # print(yaw)

            if val > 15:
                break

            pub.publish(core)
            rate.sleep()

        straight(pub,core,rate,a,time)




"""
def straight(pub,core,rate,yaw,t):

    global a
    global time
    while val < 35:
        while time - t < 10:
            while a - yaw > 10:
                core.ld = 2
                core.ls = 130
                core.rd = 1
                core.rs = 130
                # print(a-yaw)
                # print(a)
                # print(yaw)

                if w == 1:
                    break

                pub.publish(core)
                rate.sleep()

            while a - yaw < -10:

                core.ld = 1
                core.ls = 130
                core.rd = 2
                core.rs = 130
                # print(a-yaw)
                # print(a)
                # print(yaw)

                if w == 1:
                    break

                pub.publish(core)
                rate.sleep()

            core.ld = 1
            core.ls = 150
            core.rd = 1
            core.rs = 150
            # print(a-yaw)
            # print(a)
            # print(yaw)

            pub.publish(core)
            rate.sleep()
            t2 = time
        # while time - t2 < 10:

        while a - yaw < 15:

            core.ld = 2
            core.ls = 150
            core.rd = 1
            core.rs = 150
            # print(a-yaw)
            # print(a)
            # print(yaw)

            pub.publish(core)
            rate.sleep()

        while yaw - a < 30:
            core.ld = 1
            core.ls = 150
            core.rd = 2
            core.rs = 150
            # print(a-yaw)
            # print(a)
            # print(yaw)

            pub.publish(core)
            rate.sleep()

        while a - yaw < 15:
            core.ld = 2
            core.ls = 150
            core.rd = 1
            core.rs = 150
            # print(a-yaw)
            # print(a)
            # print(yaw)

            pub.publish(core)
            rate.sleep()

        straight(pub,core,rate,a,time)

"""
def turn2(pub,core,rate,yaw):
    global a

    while abs(a-yaw)<90:
        core.ld = 2
        core.ls = 110
        core.rd = 1
        core.rs = 110
        rospy.loginfo("turn")
        # print(a-yaw)
        # print(a)
        # print(yaw)

        pub.publish(core)
        rate.sleep()

    straight(pub,core,rate,a,time)


def turn(pub,core,rate,yaw):
    global a
    while abs(a-yaw)<90:

        core.ld = 1
        core.ls = 110
        core.rd = 2
        core.rs = 110
        rospy.loginfo("turh")
        # print(a-yaw)
        # print(a)
        # print(yaw)

        pub.publish(core)
        rate.sleep()

    # while w == 0:
    # 	  core.ld = 2
    #     core.ls = 250
    #     core.rd = 1
    #     core.rs = 250
    #     # print(a-yaw)
    #     # print(a)
    #     # print(yaw)

    #     pub.publish(core)
    #     rate.sleep()

    straight(pub,core,rate,a,time)

def publisher(pub):
    counter = 0
    global a
    arrow_point = Middle_list()
    core = Drive()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        arrow_point.horizontal = x
        arrow_point.vertical = y
        arrow_point.distance = z
        if arrow_point.horizontal > 330:
            core.ld = 1
            core.ls = 110
            core.rd = 2
            core.rs = 110
            rospy.loginfo("right")

            pub.publish(core)
            counter = 0
            rate.sleep()
        elif arrow_point.horizontal < 160:
            core.ld = 2
            core.ls = 110
            core.rd = 1
            core.rs = 110
            rospy.loginfo("left")

            pub.publish(core)
            counter = 0
            rate.sleep()

        else:
            if arrow_point.distance > 1500:
                core.ld = 1
                core.ls = 150
                core.rd = 1
                core.rs = 150
                rospy.loginfo("forward")

                pub.publish(core)
                counter = 0
                rate.sleep()

            else :
                core.ld = 0
                core.ls = 0
                core.rd = 0
                core.rs = 0
                rospy.loginfo("stop")
                #turn(pub,core,rate,a)
                pub.publish(core)
                counter = counter + 1
                if counter > 45:
                    if k == 1:
                        turn(pub,core,rate,a)
                    elif k == 0:
                        turn2(pub,core,rate,a)
                rate.sleep()



if __name__ == '__main__':

    pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
    subscriber()
    subscriber2()
    publisher(pub)


#check if arrow detect counter is realible enough and if it is going forward / getting increased
"""
#! /usr/bin/env python
import rospy
import cv2
import pyrealsense2
import numpy as np
import pyrealsense2 as rs
from atom_drive.msg import Middle_list   #list of two int32
from atom_drive.msg import Drive
from std_msgs.msg import Float32
from sensor_msgs.msg import Imu
import tf
import math

#a = 0
x = 0
y = 0
z = 0
val = 0

def subscriber():
    rospy.init_node('auto_calibrate',anonymous=True)
    rospy.Subscriber('forward/move',Middle_list,callback)


def subscriber2():
    rospy.Subscriber("phone1/android/imu",Imu,callback2)

def callback2(data2):
    global a
    global i
    global count
    global b

    quaternion = (data2.orientation.x, data2.orientation.y, data2.orientation.z, data2.orientation.w)
    rpy = tf.transformations.euler_from_quaternion(quaternion)
    yaw2 = rpy[2]
    yaw = math.degrees(yaw2)
    a = yaw
    # if i == 1 :
    #     b=a

    # count.append(a)

    # i=i+1

def callback(data):
    global x
    global y
    global z
    global w
    global k
    global val
    global time
    x = data.horizontal
    y = data.vertical
    z = data.distance
    w = data.detect
    k = data.direction
    time = rospy.get_time
    if data.detect == 1:
        val  = val + 1
    elif data.detect == 0:
        val = 0





def straight(pub,core,rate,yaw,t):
    global a
    global time
    while val < 20:
        #move straight for 10 secs
        #move right then left then right
    #exit

        # while time - t < 8:
        for i in range(0,100):
            core.ld = 1
            core.ls = 150
            core.rd = 1
            core.rs = 150
            rospy.loginfo("straight")
            # print(a-yaw)
            # print(a)
            # print(yaw)
            if val > 20:
                break
            pub.publish(core)
            rate.sleep()
        t = time
        # while  time - t < 10:
        while abs(a - yaw) < 10:
            core.ld = 2
            core.ls = 150
            core.rd = 1
            core.rs = 150
            rospy.loginfo("first")
            # print(a-yaw)
            # print(a)
            # print(yaw)
            if val > 20:
                break
            pub.publish(core)
            rate.sleep()
        yaw = a
        while abs(a - yaw) < 20:
            core.ld = 1
            core.ls = 150
            core.rd = 2
            core.rs = 150
            rospy.loginfo("second")
            # print(a-yaw)
            # print(a)
            # print(yaw)

            if val > 20:
                break

            pub.publish(core)
            rate.sleep()

        yaw = a

        while abs(a - yaw) < 10:
            core.ld = 2
            core.ls = 150
            core.rd = 1
            core.rs = 150
            rospy.loginfo("third")
            # print(a-yaw)
            # print(a)
            # print(yaw)

            if val > 20:
                break

            pub.publish(core)
            rate.sleep()

        straight(pub,core,rate,a,time)





def straight(pub,core,rate,yaw,t):

    global a
    global time
    while val < 35:
        while time - t < 10:
            while a - yaw > 10:
                core.ld = 2
                core.ls = 130
                core.rd = 1
                core.rs = 130
                # print(a-yaw)
                # print(a)
                # print(yaw)

                if w == 1:
                    break

                pub.publish(core)
                rate.sleep()

            while a - yaw < -10:

                core.ld = 1
                core.ls = 130
                core.rd = 2
                core.rs = 130
                # print(a-yaw)
                # print(a)
                # print(yaw)

                if w == 1:
                    break

                pub.publish(core)
                rate.sleep()

            core.ld = 1
            core.ls = 150
            core.rd = 1
            core.rs = 150
            # print(a-yaw)
            # print(a)
            # print(yaw)

            pub.publish(core)
            rate.sleep()
            t2 = time
        # while time - t2 < 10:

        while a - yaw < 15:

            core.ld = 2
            core.ls = 150
            core.rd = 1
            core.rs = 150
            # print(a-yaw)
            # print(a)
            # print(yaw)

            pub.publish(core)
            rate.sleep()

        while yaw - a < 30:
            core.ld = 1
            core.ls = 150
            core.rd = 2
            core.rs = 150
            # print(a-yaw)
            # print(a)
            # print(yaw)

            pub.publish(core)
            rate.sleep()

        while a - yaw < 15:
            core.ld = 2
            core.ls = 150
            core.rd = 1
            core.rs = 150
            # print(a-yaw)
            # print(a)
            # print(yaw)

            pub.publish(core)
            rate.sleep()

        straight(pub,core,rate,a,time)

def turn2(pub,core,rate,yaw):
    global a

    while abs(a-yaw)<90:
        core.ld = 1
        core.ls = 130
        core.rd = 2
        core.rs = 130
        rospy.loginfo("turn")
        # print(a-yaw)
        # print(a)
        # print(yaw)

        pub.publish(core)
        rate.sleep()

    straight(pub,core,rate,a,time)


def turn(pub,core,rate,yaw):
    global a
    while abs(a-yaw)<90:

        core.ld = 2
        core.ls = 130
        core.rd = 1
        core.rs = 130
        rospy.loginfo("turh")
        # print(a-yaw)
        # print(a)
        # print(yaw)

        pub.publish(core)
        rate.sleep()

    # while w == 0:
    # 	  core.ld = 2
    #     core.ls = 250
    #     core.rd = 1
    #     core.rs = 250
    #     # print(a-yaw)
    #     # print(a)
    #     # print(yaw)

    #     pub.publish(core)
    #     rate.sleep()

    straight(pub,core,rate,a,time)

def publisher(pub):
    counter = 0
    global a
    arrow_point = Middle_list()
    core = Drive()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        arrow_point.horizontal = x
        arrow_point.vertical = y
        arrow_point.distance = z
        if arrow_point.horizontal > 330:
            core.ld = 2
            core.ls = 130
            core.rd = 1
            core.rs = 130
            rospy.loginfo("right")

            pub.publish(core)
            counter = 0
            rate.sleep()
        elif arrow_point.horizontal < 160:
            core.ld = 1
            core.ls = 130
            core.rd = 2
            core.rs = 130
            rospy.loginfo("left")

            pub.publish(core)
            counter = 0
            rate.sleep()

        else:
            if arrow_point.distance > 200:
                core.ld = 1
                core.ls = 150
                core.rd = 1
                core.rs = 150
                rospy.loginfo("forward")

                pub.publish(core)
                counter = 0
                rate.sleep()

            else :
                core.ld = 0
                core.ls = 0
                core.rd = 0
                core.rs = 0
                rospy.loginfo("stop")
                #turn(pub,core,rate,a)
                pub.publish(core)
                counter = counter + 1
                if counter > 45:
                    if k == 1:
                        turn(pub,core,rate,a)
                    elif k == 0:
                        turn2(pub,core,rate,a)
                rate.sleep()



if __name__ == '__main__':

    pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
    subscriber()
    subscriber2()
    publisher(pub)

"""
