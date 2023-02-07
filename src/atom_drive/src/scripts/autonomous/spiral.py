#! /usr/bin/env python 
import rospy
from atom_drive.msg import Arrow
from atom_drive.msg import Drive
from sensor_msgs.msg import Imu


def subscriber():
    rospy.init_node('expanding_spiral',anonymous=True)
    rospy.Subscriber('arrow/detect', Arrow, callback)

i = 0

def callback(data):
    global x
    global i
    global time
    global yaw
    yaw = data.yaw
    time = rospy.get_time()
    x = data.data
    i = i+1

def turn(pub,core,rate,yaw2):
    while (yaw-yaw2) < 90:
        core.ld = 2
        core.ls = 150
        core.rd = 1
        core.rs = 150

        pub.publish(core)
        rate.sleep()


count = 1
time_turn = 0 
def publisher(pub):
    global time_turn
    global time_interval
    global count
    rospy.loginfo('connected')
    
    rate = rospy.Rate(10)
    core = drive()
    if x == 1:
        while not rospy.is_shutdown():
            if count%2 == 1:
                time_interval = 10*count
                time_turn = time_turn + time_interval
                count = count + 1
                if (time - time_turn - 23*(count-1)) < 0.1: # 23 -> time taken to turn , count - 1 -> number of turns that have happened 
                    turn(pub2,core,rate,yaw) #publishing message
            if count%2 == 0 :
                time_interval = 7*count
                time_turn = time_turn + time_interval
                count = count + 1
                if (time - time_turn - 23*(count - 1)) < 2:
                    turn(pub,core,rate,yaw)

            # if time == 34 + previous time:  write 34 as a function of count and time 

            # if count even - relatively shorter spurt - shorter time span inscrease
            #     turn right
            # at certain time - publish a boolean yes to some topic which turn right 
            #subscribes to indicate/tell it to start turn right
            else:
                core.ld = 2
                core.ls = 150
                core.rd = 2
                core.rs = 150

                pub.publish(core)
                rate.sleep()


    # if time > 10 :



if __name__ == '__main__':
    pub = rospy.Publisher('spiral/move',Drive,queue_size = 20)
    
    subscriber()
    publisher(pub)