#! /use/bin/env python
import rospy
from atom_drive.msg import Sensors.msg


def callback(data):
    global x,y,z,w,a,b,c,d,m,n,o,p
    x = data.temperature
    y = data.humidity
    z = data.pressure
    w = data.uva
    a = data.uvb
    b = data.uvindex
    c = data.N 
    d = data.P 
    m = data.K
    n = data.soiltemp
    o = data.soilmoist
    p = data.soilph



def listener():
    rospy.init_node('Listener',anonymous=True)
    rospy.Subscriber("topic_name",Sensors,callback)
    rospy.spin()

if __name__=='__main__':
    listener()
