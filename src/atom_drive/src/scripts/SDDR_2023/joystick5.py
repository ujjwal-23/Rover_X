#! /usr/bin/env python
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

    def core_callback(self, data):
        self.axes = list(data.axes)
        self.buttons = list(data.buttons)

    def set_nav_values(self):

        '''sets values for array to send STM1 for navigaion '''

        # # Turn Left 
         #if  self.axes[0]>0 and self.axes[1]>0:
         #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
         #    self.LD = 1 
         #    self.RD = 1
         #    self.LS = int(high_speed/2)
         #    self.RS = int(high_speed)
        # # Turn Right
         #elif self.axes[0]<0 and self.axes[1]>0:
         #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
         #    self.LD = 1 
         #    self.RD = 1
         #    self.LS = int(high_speed)
         #    self.RS = int(high_speed/2)
        # # Turn Reverse Right
         #elif self.axes[0]>0 and self.axes[1]<0:
         #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
         #    self.LD = 2 
         #    self.RD = 2
         #    self.LS = int(high_speed/2)
         #    self.RS = int(high_speed)
        # # Turn Reverse Left
         #elif self.axes[0]<0 and self.axes[1]<0:
         #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
         #    self.LD=2
         #    self.RD=2
         #    self.LS=int(high_speed)
         #    self.RS=int(high_speed/2)
        # Forward
        if self.axes[1]>0: 
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

        
    
    def limit_value(self, value, low, high):
        if value < low:
            value = low
        if value > high:
            value = high
        return value


