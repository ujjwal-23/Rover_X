#! /usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix

def subscriber():
    rospy.init_node('gps_map',anonymous=True)
    rospy.Subscriber("gps/data",NavSatFix,callback)

def callback(data):
    global x
    global y

    x = data.latitude
    y = data.longitude

def publisher(pub):
    rate = rospy.Rate(10)
    core = NavSatFix()

    while not rospy.is_shutdown():
        core.latitude = x
        core.longitude = y

        pub.publish(core)
        rate.sleep()

if __name__=='__main__':
    pub = rospy.Publisher('mapviz/data', NavSatFix , queue_size=20)
    subscriber()
    publisher(pub)