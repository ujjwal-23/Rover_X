#! /usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
import math


def publisher(pub):
    rospy.init_node('mapviz_data',anonymous = True)
    rate = rospy.Rate(10)
    core = NavSatFix()

    for j in range(0,n-1):
        a=gps[j]
        b=gps[j+1]
        c=gps[j]
        step1 = (b[0]-a[0])/200
        step2 = (b[1]-a[1])/200
        # while not rospy.is_shutdown():
        for i in range(0,200):
            core.latitude = c[0]
            core.longitude = c[1]
            c[0] = c[0] - step1
            c[1] = c[1] - step2
            pub.publish(core)
            rate.sleep()


if __name__=='__main__':
    # global gps
    # global a
    # global b
    # a = [12.6789,133.3765]
    # b = [14.6734,135.2355]
    n=int(input())
    gps=[]
    gps2=[]
    for i in range(0,n-1):
        data=input()
        raw=data.split(',')
        gps.append(data)
        gps2.append(tuple(raw))
    pub=rospy.Publisher('some/topic', NavSatFix ,queue_size = 20)
    # for j in range(0,n-1):
    publisher(pub)
    # publisher(pub)
