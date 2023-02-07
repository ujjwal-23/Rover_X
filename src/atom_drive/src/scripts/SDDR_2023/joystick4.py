#! /usr/bin/env python
from atom_drive import msg
import rospy
from sensor_msgs.msg import Joy
from atom_drive.msg import Arm
from std_msgs.msg import Int32MultiArray
import time


class Joystick:
    def __init__(self) -> None:

        # rospy.init_node('joystick_node', anonymous=True)
        rospy.Subscriber('joy1', Joy, self.core_callback)

        self.axes = [0, 0, 0, 0, 0, 0]
        self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.BASE_SPEED = 0
        self.BASE_DIR = 0 
        self.SHOULDER_SPEED = 0
        self.SHOULDER_DIR = 0
        self.ELBOW_SPEED = 0
        self.ELBOW_DIR = 0
        self.YAW_SPEED = 0
        self.YAW_DIR = 0
        self.PITCH_SPEED = 0
        self.PITCH_DIR = 0
        self.ROLL_SPEED = 0
        self.ROLL_DIR = 0
        self.END_EFF_SPEED = 0
        self.END_EFF_DIR = 0
        self.SET_MODE = 0
        self.SOL_DIR = 0
        

    def core_callback(self, data):
        self.axes = list(data.axes)
        self.buttons = list(data.buttons)

    # def set_nav_values(self):

    #     '''sets values for array to send STM1 for navigaion '''

    #     # Turn Left 
    #     if  self.axes[0]>0 and self.axes[1]>0:
    #         high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
    #         self.LD = 1 
    #         self.RD = 1
    #         self.LS = int(high_speed/2)
    #         self.RS = int(high_speed)
    #     # Turn Right
    #     elif self.axes[0]<0 and self.axes[1]>0:
    #         high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
    #         self.LD = 1 
    #         self.RD = 1
    #         self.LS = int(high_speed)
    #         self.RS = int(high_speed/2)
    #     # Turn Reverse Right
    #     elif self.axes[0]>0 and self.axes[1]<0:
    #         high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
    #         self.LD = 2 
    #         self.RD = 2
    #         self.LS = int(high_speed/2)
    #         self.RS = int(high_speed)
    #     # Turn Reverse Left
    #     elif self.axes[0]<0 and self.axes[1]<0:
    #         high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
    #         self.LD=2
    #         self.RD=2
    #         self.LS=int(high_speed)
    #         self.RS=int(high_speed/2)
    #     # Forward
    #     elif self.axes[1]>0: 
    #         self.LD=1
    #         self.RD=1
    #         self.LS=int(abs(self.axes[1]*250))
    #         self.RS=int(abs(self.axes[1]*250))
    #     # Backward
    #     elif self.axes[1]<0:
    #         self.LD=2
    #         self.RD=2
    #         self.LS=int(abs(self.axes[1]*250))
    #         self.RS=int(abs(self.axes[1]*250))
    #     # Left
    #     elif self.axes[0]>0: 
    #         self.LD=2
    #         self.RD=1
    #         self.LS=int(abs(self.axes[0]*250))
    #         self.RS=int(abs(self.axes[0]*250))
    #     # Right
    #     elif self.axes[0]<0: #right
    #         self.LD=1
    #         self.RD=2
    #         self.LS=int(abs(self.axes[0]*250))
    #         self.RS=int(abs(self.axes[0]*250))
    #     # Default zero
    #     if self.axes[0] == 0 and self.axes[1] == 0:
    #         self.LD = 0
    #         self.RD = 0
    #         self.LS = 0
    #         self.RS = 0

        
    def set_arm_values(self):

        '''sets the angle values for the arm'''

        # change_base_value
        if self.axes[0]>0 and self.axes[1] == 0: 
            self.BASE_DIR=1
            self.BASE_SPEED = int(abs(self.axes[0]*250))

        elif self.axes[0]<0 and self.axes[1] == 0:
             self.BASE_DIR=2
             self.BASE_SPEED = int(abs(self.axes[0]*250))
        
        #change_shoulder_values
        if self.axes[1]>0 and self.axes[0] == 0: 
            self.SHOULDER_DIR=1
            self.SHOULDER_SPEED = int(abs(self.axes[1]*250))

        elif self.axes[1]<0 and self.axes[0] == 0:
             self.SHOULDER_DIR=2
             self.SHOULDER_SPEED = int(abs(self.axes[1]*250))
        
        #change_elbow_values
        if self.axes[3]>0: 
            self.ELBOW_DIR=1
            self.ELBOW_SPEED = int(abs(self.axes[3]*250))

        elif self.axes[3]<0:
             self.ELBOW_DIR=2
             self.ELBOW_SPEED = int(abs(self.axes[3]*250))


        #change_yaw_values
        if self.axes[2]>0: 
            self.YAW_DIR=1
            self.YAW_SPEED = int(abs(self.axes[2]*250))

        elif self.axes[2]<0:
             self.YAW_DIR=2
             self.YAW_SPEED = int(abs(self.axes[2]*250))

        #change_pitch_value
        if self.buttons[6] == 1: 
            self.PITCH_DIR=1
            self.PITCH_SPEED = 250

        elif self.buttons[7] == 1:
             self.PITCH_DIR=2
             self.PITCH_SPEED = 250

        #change_roll_value
        if self.axes[4] == 1: 
            self.ROLL_DIR=1
            self.ROLL_SPEED = 250

        elif self.axes[4] == -1:
            self.ROLL_DIR=2
            self.ROLL_SPEED = 250

        #change_endfactor_value
        if self.axes[5] == 1: 
            self.END_EFF_DIR=1
            self.END_EFF_SPEED = 250

        elif self.axes[5] == -1:
            self.END_EFF_DIR=2
            self.END_EFF_SPEED = 250

        if self.buttons[1] == 1:
        	self.SOL_DIR=1

        #default_zero_left_axis

        if self.axes[0] == 0 and self.axes[1] == 0:
            self.BASE_DIR = 0
            self.BASE_SPEED = 0
            self.SHOULDER_DIR = 0
            self.SHOULDER_SPEED = 0

        ##default_zero_right_axis
        if self.axes[2] == 0 and self.axes[3] == 0:
            self.ELBOW_DIR = 0
            self.ELBOW_SPEED = 0
            self.YAW_DIR = 0
            self.YAW_SPEED = 0

        #default_extra_axis
        if self.axes[4] == 0 and self.axes[5] == 0:
            self.END_EFF_DIR = 0
            self.END_EFF_SPEED = 0
            self.ROLL_DIR = 0
            self.ROLL_SPEED = 0
        
        #default_endfactor_value
        if self.buttons[6] == 0 and self.buttons[7] == 0: 
            self.PITCH_DIR = 0
            self.PITCH_SPEED = 0

        if self.buttons[1] == 0:
        	self.SOL_DIR=0
            

        	
        
    
    def set_mode(self):

        '''Toggle between normal mode and kids mode'''

        if self.buttons[3] == 1:
            self.SET_MODE = 0
            rospy.loginfo("NORMAL MODE")
        if self.buttons[2] == 1:
            self.SET_MODE = 1
            rospy.loginfo("PRECISION MODE")
    

    def limit_value(self, value, low, high):
        if value < low:
            value = low
        if value > high:
            value = high
        return value
