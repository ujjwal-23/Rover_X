#! /usr/bin/env python
from math import ldexp
import rospy
from sensor_msgs.msg import Joy
from atom_drive.msg import Core
from std_msgs.msg import Int32MultiArray
import time


class Joystick:
    def __init__(self) -> None:

        # rospy.init_node('joystick_node', anonymous=True)
        rospy.Subscriber('joy0', Joy, self.core_callback)

        self.axes = [0, 0, 0, 0, 0, 0]
        self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.LD = 0
        self.RD = 0
        self.LS = 0
        self.RS = 0
        self.SET_MODE = 0
        self.RAMAN_DIRECTION_V = 0
        self.RAMAN_SPEED_V = 0
        self.RAMAN_DIRECTION_H = 0
        self.RAMAN_SPEED_H = 0
        self.DRILL_DIRECTION = 0
        self.DRILL_SPEED = 0
        self.AUGER_DIRECTION = 0
        self.H_AUGER_DIRECTION = 0
        self.CAROUSEL_DIRECTION = 0
        self.CAROUSEL_SPEED = 0
        self.REAGENT_DIRECTION = 0
        self.SERVO = 0
        


        

    def core_callback(self, data):
        self.axes = list(data.axes)
        self.buttons = list(data.buttons)

    def set_nav_values(self):

        '''sets values for array to send STM1 for navigaion '''

        # Turn Left 
        if  self.axes[0]>0 and self.axes[1]>0:
            high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
            self.LD = 1 
            self.RD = 1
            self.LS = int(high_speed/2)
            self.RS = int(high_speed)
        # Turn Right
        elif self.axes[0]<0 and self.axes[1]>0:
            high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
            self.LD = 1 
            self.RD = 1
            self.LS = int(high_speed)
            self.RS = int(high_speed/2)
        # Turn Reverse Right
        elif self.axes[0]>0 and self.axes[1]<0:
            high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
            self.LD = 2 
            self.RD = 2
            self.LS = int(high_speed/2)
            self.RS = int(high_speed)
        # Turn Reverse Left
        elif self.axes[0]<0 and self.axes[1]<0:
            high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
            self.LD=2
            self.RD=2
            self.LS=int(high_speed)
            self.RS=int(high_speed/2)
        # Forward
        elif self.axes[1]>0: 
            self.LD=1
            self.RD=1
            self.LS=int(abs(self.axes[1]*250))
            self.RS=int(abs(self.axes[1]*250))
        # Backward
        elif self.axes[1]<0:
            self.LD=2
            self.RD=2
            self.LS=int(abs(self.axes[1]*250))
            self.RS=int(abs(self.axes[1]*250))
        # Left
        elif self.axes[0]>0: 
            self.LD=2
            self.RD=1
            self.LS=int(abs(self.axes[0]*250))
            self.RS=int(abs(self.axes[0]*250))
        # Right
        elif self.axes[0]<0: #right
            self.LD=1
            self.RD=2
            self.LS=int(abs(self.axes[0]*250))
            self.RS=int(abs(self.axes[0]*250))
        # Default zero
        if self.axes[0] == 0 and self.axes[1] == 0:
            self.LD = 0
            self.RD = 0
            self.LS = 0
            self.RS = 0

    def set_science_values(self):
        '''Sets the array values for the science task'''
        if self.SET_MODE == 0:
        #Raman Controls

            # UP
            if self.axes[3]>0: 
                self.RAMAN_DIRECTION_V=1
                self.RAMAN_SPEED_V=int(abs(self.axes[3]*250))
            # DOWN
            elif self.axes[3]<0: 
                self.RAMAN_DIRECTION_V=2
                self.RAMAN_SPEED_V=int(abs(self.axes[3]*250))
            # Left
            if self.axes[2] > 0:
                self.RAMAN_DIRECTION_H = 1
                self.RAMAN_SPEED_H = int(abs(self.axes[2]*250))

            # Right
            elif self.axes[2] < 0:
                self.RAMAN_DIRECTION_H = 2
                self.RAMAN_SPEED_H = int(abs(self.axes[2]*250))
            #servo 
            if self.axes[5] == -1 :
                self.SERVO = 1
            elif self.axes[5]== 1:
                self.SERVO = 0
            

            #stationary
            if self.axes[2] == 0 and self.axes[3] == 0:
                self.RAMAN_DIRECTION_H = 0
                self.RAMAN_SPEED_H = 0
                self.RAMAN_DIRECTION_V = 0
                self.RAMAN_SPEED_V = 0



        if self.SET_MODE == 1:
        #Drill Controls

            #Drill_up
            if self.axes[3]>0: 
                self.DRILL_DIRECTION=1
                self.DRILL_SPEED=int(abs(self.axes[3]*250))
            #Drill_down 
            elif self.axes[3]<0: 
                self.DRILL_DIRECTION=2
                self.DRILL_SPEED=int(abs(self.axes[3]*250))
            if self.axes[3] == 0:
                self.DRILL_DIRECTION = 0
                self.DRILL_SPEED = 0
            #vertical_Auger
            if self.buttons[5] == 1:
                self.AUGER_DIRECTION = 1
            elif self.buttons[4] == 1:
                self.AUGER_DIRECTION = 2
            if (self.buttons[5] == 0 and self.buttons[4] == 0):
                self.AUGER_DIRECTION = 0
            #Horizontal_Auger
            if self.buttons[7] ==1:
                self.H_AUGER_DIRECTION = 1
            if self.buttons[6] ==1:
                self.H_AUGER_DIRECTION = 2
            if (self.buttons[6] == 0 and self.buttons[7] == 0):
                self.H_AUGER_DIRECTION = 0
            
        if self.SET_MODE == 2:
        #Sampling_controls

            #carousel
            if self.axes[2] < 0:
                self.CAROUSEL_DIRECTION = 1
                self.CAROUSEL_SPEED = int(abs(self.axes[2]*250))
            elif self.axes[2] > 0:
                self.CAROUSEL_DIRECTION = 2
                self.CAROUSEL_SPEED = int(abs(self.axes[2]*250))
            if self.axes[2] == 0:
                self.CAROUSEL_DIRECTION = 0
                self.CAROUSEL_SPEED = 0
            
            #reagent
            if self.buttons[5] == 1:
                self.REAGENT_DIRECTION = 1
            elif self.buttons[4] == 1:
                self.REAGENT_DIRECTION = 2
            if self.buttons[5] == 0 and self.buttons[4] == 0:
                self.REAGENT_DIRECTION = 0
        

    def set_mode(self):

        '''Toggle between Raman, Drill, Sampling'''

        if self.buttons[3] == 1:
            self.SET_MODE = 0
            rospy.loginfo("RAMAN MODE")
        if self.buttons[2] == 1:
            self.SET_MODE = 1
            rospy.loginfo("DRILL MODE")
        if self.buttons[1] == 1:
            self.SET_MODE = 2
            rospy.loginfo("SAMPLING MODE")
        if self.buttons[0] == 1:
            self.SET_MODE  = 3
            rospy.loginfo("KIDS MODE")

    def limit_value(self, value, low, high):
        if value < low:
            value = low
        if value > high:
            value = high
        return value







