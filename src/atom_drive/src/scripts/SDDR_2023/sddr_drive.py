#! /usr/bin/env python
import rospy
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Joy
from atom_drive.msg import Drive
from joystick5 import Joystick


def publish_values_joy(pub):
    
    rospy.loginfo("Base station publishing values via Joystick")

    loop_rate = rospy.Rate(10)
    core = Drive()
    
    while not rospy.is_shutdown():
        # if len(joystick.axes)  > 6:
        #     rospy.logfatal("Terminating....... \n Joystick set to XInput mode configure it for DInput mode")
        #     return 0
        joystick.set_nav_values()
        core.ld = joystick.LD
        core.ls = joystick.LS
        core.rd = joystick.RD
        core.rs = joystick.RS

        
        pub.publish(core)
        loop_rate.sleep()

if __name__ == '__main__':

    rospy.init_node('atom_nav_data')
    joystick = Joystick()
    pub = rospy.Publisher('atom/nav_data', Drive, queue_size = 20)
    
    publish_values_joy(pub)


    
    

