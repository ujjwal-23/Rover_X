#! /usr/bin/env python
import rospy
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Joy
from atom_drive.msg import Core
from joystick1 import Joystick


def publish_values_joy(pub):
    
    rospy.loginfo("Base station publishing values via Joystick")

    loop_rate = rospy.Rate(10)
    core = Core()
    
    while not rospy.is_shutdown():
        # if len(joystick.axes)  > 6:
        #     rospy.logfatal("Terminating....... \n Joystick set to XInput mode configure it for DInput mode")
        #     return 0
        joystick.set_nav_values()
        joystick.set_mode()

        core.mode = joystick.SET_MODE
        core.ld = joystick.LD
        core.ls = joystick.LS
        core.rd = joystick.RD
        core.rs = joystick.RS

        if joystick.SET_MODE == 0:
            joystick.set_arm_values()

            core.base = joystick.BASE
            core.shoulder = joystick.SHOULDER
            core.elbow = joystick.ELBOW
            core.wrist = joystick.WRIST
            core.gripper = joystick.GRIPPER 
        
        if joystick.SET_MODE == 2:
            publish_values_ik(pub)
        
        pub.publish(core)
        loop_rate.sleep()

############## This function will be defined in the other file in some other class ############
def publish_values_ik(pub):                                                                   
    pass                                                                                      

    

if __name__ == '__main__':

    rospy.init_node('atom_core_data')
    joystick = Joystick()
    pub = rospy.Publisher('atom/core_data', Core, queue_size = 10)

    if joystick.SET_MODE == 0:
        publish_values_joy(pub)
    elif joystick.SET_MODE == 2:
        publish_values_ik(pub)
    
    


    
    

