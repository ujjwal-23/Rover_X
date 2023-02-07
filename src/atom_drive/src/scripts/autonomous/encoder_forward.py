#! /usr/bin/env python


#using encoder data while moving forward(already in forward motion) to pevent a drift 
#initially , every motor is given full and EQUAL pwm i.e. 255,255,255
import rospy
from atom_drive.msg import Pid 
import numpy as np

def subscriber():
    rospy.init_node('encoder_data',anonymous=True)
    rospy.Subscriber("encoder/data", Pid, callback)

def callback(data):
    global x,y,z,w
    x,y,z,w = (data.lf ,data.lb, data.rf, data.rb)

def publisher(pub):
    rospy.loginfo("connected")
    rate = rospy.Rate(10)
    core = Pwm()

    while not rospy.is_shutdown():
        core.lfd,core.lbd,core.rfd,core.rbd = 2,2,2,2
        k=min(x,y,z,w)
        #x,y,z,w = k, k, k, k
        #new pwm = 255 - ((y-k)/y)*255
        core.lfs = 255 - ((x-k)/x)*255
        core.lbs = 255 - ((y-k)/y)*255
        core.rfs = 255 - ((z-k)/z)*255
        core.rbs = 255 - ((w-k)/w)*255

        pub.publish(core)
        rate.sleep()




if __name__=='__main__':

    pub = rospy.Publisher('forward/move', Pwm, queue_size = 20)
    subscriber()
    publisher(pub)

