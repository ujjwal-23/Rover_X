#! /usr/bin/env python

import rospy
from std_msgs.msg import Int32MultiArray
from atom_drive.msg import Core
from sensor_msgs.msg import Joy
from PyQt5 import QtWidgets,uic
import time

'''This ROS Node converts Joystick inputs from the joy node
into commands for turtlesim or any other robot

Receives joystick messages (subscribed to Joy topic)
then converts the joysick inputs into array commands
axis 1 aka left stick vertical controls linear speed
axis 0 aka left stick horizonal controls angular speed'''

BASE, SHOULDER, ELBOW, WRIST, GRIPPER = 0, 0, 0, 0, 0
LD, LS, RD, RS = 0, 0, 0, 0
SET_MODE = 0

axes, buttons = [0,0,0,0,0,0,0,0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def limit_value(value):
    if value < 0:
        value = 0
    if value > 360:
        value = 360
    return value 


def core_callback(data):

    global axes, buttons
 
    axes = list(data.axes)
    buttons = list(data.buttons)


def reset_arm():
    global BASE 
    global SHOULDER
    global ELBOW 
    global WRIST 
    global GRIPPER 

    BASE, SHOULDER, ELBOW, WRIST, GRIPPER = 0, 0, 0, 0, 0


def make_array(pub):
    global axes
    global buttons
    global SET_MODE
    global LD
    global LS
    global RD
    global RS
    loop_rate = rospy.Rate(10)
    core=Core()

    while not rospy.is_shutdown():
        rospy.loginfo_once("Base station is publising values")
        if buttons[1] == 1:
            SET_MODE = 0
            rospy.loginfo("ARM MODE SET")
        if buttons[0] == 1:
            SET_MODE = 1
            rospy.loginfo("SCIENCE MODE SET")

        # creating an array for the motion of the Rover

        if  axes[0]>0 and axes[1]>0:
            high_speed=(int(abs(axes[0]*250))+int(abs(axes[1]*250)))/2
            LD = 1 
            RD = 1
            LS = int(high_speed/2)
            RS = int(high_speed)

        elif axes[0]<0 and axes[1]>0:
            high_speed=(int(abs(axes[0]*250))+int(abs(axes[1]*250)))/2
            LD = 1 
            RD = 1
            LS = int(high_speed)
            RS = int(high_speed/2)

        elif axes[0]>0 and axes[1]<0:
            high_speed=(int(abs(axes[0]*250))+int(abs(axes[1]*250)))/2
            LD = 2 
            RD = 2
            LS = int(high_speed/2)
            RS = int(high_speed)

        elif axes[0]<0 and axes[1]<0:
            high_speed=(int(abs(axes[0]*250))+int(abs(axes[1]*250)))/2
            LD=2
            RD=2
            LS=int(high_speed)
            RS=int(high_speed/2)
        
        elif axes[1]>0: 
            LD=1
            RD=1
            LS=int(abs(axes[1]*250))
            RS=int(abs(axes[1]*250))

        elif axes[1]<0:
            LD=2
            RD=2
            LS=int(abs(axes[1]*250))
            RS=int(abs(axes[1]*250))

        elif axes[0]>0: #left
            LD=2
            RD=1
            LS=int(abs(axes[0]*250))
            RS=int(abs(axes[0]*250))

        elif axes[0]<0: #right
            LD=1
            RD=2
            LS=int(abs(axes[0]*250))
            RS=int(abs(axes[0]*250))

        if axes[0] == 0 and axes[1] == 0:
            LD = 0
            RD = 0
            LS = 0
            RS = 0
        
        core.ld = LD
        core.ls = LS
        core.rd = RD
        core.rs = RS
     
        if SET_MODE == 0:
            global BASE
            global SHOULDER
            global ELBOW
            global WRIST
            global GRIPPER

            # increase_base_value
            if axes[2] == -1:
                BASE += 1
            # decrease_base_value
            elif axes[2] == 1:
                BASE -= 1

            # increase_shoulder_value
            elif axes[3] == 1:
                SHOULDER += 1
            # decrease_shoulder_value_
            elif axes[3] == -1:
                SHOULDER -= 1

            # increase_elbow_value
            if axes[4] == -1:
                ELBOW += 1
            # decrease_elbow_value
            elif axes[4] == 1:
                ELBOW -= 1
            
            # increase_wrist_pitch_value
            elif axes[5] == 1:
                WRIST += 1
            # decrease_wrist_pitch_value
            elif axes[5] == -1:
                WRIST -= 1

            # increase_the_Grip
            if buttons[6] == 1:
                GRIPPER += 1
            # decrease_the_Grip 
            elif buttons[4] == 1:
                GRIPPER -= 1

            #setting_values_between_0_360
            BASE = limit_value(BASE)
            SHOULDER = limit_value(SHOULDER)
            ELBOW = limit_value(ELBOW)
            WRIST = limit_value(WRIST)
            GRIPPER = limit_value(GRIPPER)

            #reset_arm_position
            if buttons[5] == 1:
                reset_arm()

            core.base = BASE
            core.shoulder = SHOULDER
            core.elbow = ELBOW
            core.wrist = WRIST
            core.gripper = GRIPPER



        #rospy.loginfo(core)
        pub.publish(core)
        # display_array()
        loop_rate.sleep()

# def display_array():
#     call.ld.display(LD)
#     call.rd.display(RD)
#     call.ls.display(LS)
#     call.rs.display(RS)


# Intializes everything
def start():

    pose_subscriber = rospy.Subscriber('joy', Joy, core_callback)
    pub = rospy.Publisher('atom/core_data', Core, queue_size = 10)
    # subscribed to joystick inputs on topic "joy"
    # starts the node
    rospy.init_node('atom_core_data')
    make_array(pub)
    rospy.spin()

if __name__ == '__main__':
    
    start()



    









    
