#! /usr/bin/env python
import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Float32
from atom_drive.msg import Drive
from sensor_msgs.msg import Imu
import numpy as np
import tf
import math




def listener():
    rospy.init_node('Auto_turn',anonymous=True)
    #rospy.Subscriber("imu/data_raw",Float32,callback)
    rospy.Subscriber("phone1/android/imu",Imu,callback)
    # rospy.spin()




i = 0
count = []
x=0
y=0
def callback(data):
    #print(data.data)
    global x
    global i
    global count
    global y

    quaternion = (data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)
    rpy = tf.transformations.euler_from_quaternion(quaternion)
    yaw2 = rpy[2]
    yaw = math.degrees(yaw2)
    x = yaw
    if i == 1 :
        y=x
    #rospy.loginfo("%dcounter"%i)
    count.append(x)
    #rospy.loginfo("%dindex"%len(count))
    i=i+1




    # rospy.loginfo("connected")
    # rate=rospy.Rate(10)
    # core = Drive()

    # core.ld = 2
    # core.ls = 255
    # core.rd = 1
    # core.rs = 255

    # pub.publish(core)
    # # rate.sleep()

def talker(pub):

    rospy.loginfo("connected")
    rate=rospy.Rate(10)
    core = Drive()
    
    while not rospy.is_shutdown():
        rospy.loginfo("x-y= %f"%abs(x-y))
        rospy.loginfo("x= %f"%x)
        rospy.loginfo("y= %f"%y)
        if abs(x-y)<90:
            core.ld = 2
            core.ls = 150
            core.rd = 1
            core.rs = 150

            pub.publish(core)
            rospy.loginfo("data sent = (%d, %d, %d, %d)",core.ld,core.ls,core.rd,core.rs)
            rate.sleep()
        else:
            core.ld = 0
            core.ls = 0
            core.rd = 0
            core.rs = 0

            pub.publish(core)
            rospy.loginfo("data sent = (%d, %d, %d, %d)",core.ld,core.ls,core.rd,core.rs)
            rate.sleep()            

"""
def talker2(pub):

    rate=rospy.Rate(10)
    core = Drive()
    while not rospy.is_shutdown():
        core.ld = 0
        core.ls = 0
        core.rd = 0
        core.rs = 0

        pub.publish(core)
        rate.sleep()
"""

if __name__=='__main__':

    pub=rospy.Publisher('turn/auto', Drive, queue_size = 20)
    print(x)
    listener()
    #rate=rospy.Rate(10)
    #rate.sleep()
    talker(pub)
    #talker(pub)
    """
    if abs(x-180)<90:
        talker(pub)
        print(x)
    else:
        talker2(pub)
    """
    




"""
    if ((x-count[0])<90):
        try:
            talker()
        except rospy.ROSInterruptException:
            pass
    else:
        try:
            talker2()
        except rospy.ROSInterruptException:
            pass      
""" 




"""
#! /usr/bin/env python
import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Float32
from atom_drive.msg import Drive
import numpy as np




def listener():
    rospy.init_node('Listener',anonymous=True)
#    global i
#    i = -1
    rospy.Subscriber("imu/data_raw",Float32,callback)
    rospy.spin()




i = -1
count = []
def callback(data):
    print(data.data)
    global x
    global i
    global count
#    DATA = data.item()
    x = data.data


    rospy.loginfo("%dcounter"%i)
    
    count.append(x)
#    rospy.loginfo("%f"%HELLO)
    rospy.loginfo("%dindex"%len(count))
#    count[i]=data
    i=i+1

    try:
        talker()
    except rospy.ROSInterruptException:
        pass

    if (count[i]-count[0]) < 90:
        try:
            talker()
        except rospy.ROSInterruptException:
            pass
    else:
        try:
            talker2()
        except rospy.ROSInterruptException:
            pass



def talker():
    pub=rospy.Publisher('turn/auto', Drive, queue_size = 20)
    rospy.loginfo("connected")
    rate=rospy.Rate(10)
    core = Drive()

    #while not rospy.is_shutdown():
    core.ld = 2
    core.ls = 255
    core.rd = 1
    core.rs = 255

    pub.publish(core)
    rate.sleep()

def talker2():

    pub=rospy.Publisher('turn/auto', Drive, queue_size = 20)
#    rospy.loginfo("connected")
    rate=rospy.Rate(10)
    core = Drive()
    
    # while not rospy.is_shutdown():
    core.ld = 0
    core.ls = 0
    core.rd = 0
    core.rs = 0

    pub.publish(core)
    rate.sleep()



def publish_values_joy(pub):
    rospy.loginfo("connected")
    loop_rate = rospy.Rate(10)
    core = Drive()
    rospy.init_node('atom_nav_data')

    pub = rospy.Publisher('turn/auto', Drive, queue_size = 20)
    
    publish_values_joy(pub)


if __name__=='__main__':
#    i=-1
#    global pub
#    pub=rospy.Publisher('turn/auto', Drive, queue_size = 20)
    listener()

"""

