#! /usr/bin/env python
import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Float32
from atom_drive.msg import Drive
import numpy as np




def listener():
    rospy.init_node('Auto_turn',anonymous=True)
    rospy.Subscriber("imu/data_raw",Float32,callback)
    # rospy.spin()




i = 0
count = []
x=0
def callback(data):
    #print(data.data)
    global x
    global i
    global count
    x = data.data
    rospy.loginfo("%dcounter"%i)
    count.append(x)
    rospy.loginfo("%dindex"%len(count))
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
        if abs(x-180)<90:
            core.ld = 2
            core.ls = 255
            core.rd = 1
            core.rs = 255

            pub.publish(core)
            rate.sleep()
        else:
            core.ld = 0
            core.ls = 0
            core.rd = 0
            core.rs = 0

            pub.publish(core)
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
