#! /usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from atom_drive.msg import Core
from std_msgs.msg import Int32MultiArray
import time


class Joystick:
    def __init__(self) -> None:

        # rospy.init_node('joystick_node', anonymous=True)
        rospy.Subscriber('joy', Joy, self.core_callback)

        self.axes = [0, 0, 0, 0, 0, 0]
        self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.LD = 0
        self.RD = 0
        self.LS = 0
        self.RS = 0
        self.BASE = 0
        self.SHOULDER = 0 
        self.ELBOW = 0
        self.WRIST = 0
        self.GRIPPER = 0
        self.SET_MODE = 0
        self.DRILL_STATE = 0
        self.DRILL_DISTANCE = 0
        self.DRILL_SPEED = 0
        self.AUGER_STATE = 0
        self.CAROUSEL = 0
        self.REAGENT = 0


        

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

        
    def set_arm_values(self):

        '''sets the angle values for the arm'''

        # increase_base_value
        if self.axes[2] == -1:
            self.BASE += 1
        # decrease_base_value
        elif self.axes[2] == 1:
            self.BASE -= 1

        # increase_shoulder_value
        elif self.axes[3] == 1:
            self.SHOULDER += 1
        # decrease_shoulder_value_
        elif self.axes[3] == -1:
            self.SHOULDER -= 1

        # increase_elbow_value
        if self.axes[4] == -1:
            self.ELBOW += 1
        # decrease_elbow_value
        elif self.axes[4] == 1:
            self.ELBOW -= 1
        
        # increase_wrist_pitch_value
        elif self.axes[5] == 1:
            self.WRIST += 1
        # decrease_wrist_pitch_value
        elif self.axes[5] == -1:
            self.WRIST -= 1

        # increase_the_Grip
        if self.buttons[6] == 1:
            self.GRIPPER += 1
        # decrease_the_Grip 
        elif self.buttons[4] == 1:
            self.GRIPPER -= 1
        
        if self.buttons[5] == 1:
            self.reset_arm()
        
        self.BASE = self.limit_value(self.BASE, low=0, high=360)
        self.SHOULDER = self.limit_value(self.SHOULDER, low=0, high=360)
        self.ELBOW = self.limit_value(self.ELBOW, low=0, high=360)
        self.WRIST = self.limit_value(self.WRIST, low=0, high=360)
        self.GRIPPER = self.limit_value(self.GRIPPER, low=0, high=360)


    def set_science_values(self):
        '''Sets the array values for the science task'''
        self.SET_MODE = 1  
        
        #URC CODE 
        # increase_carousel_number
        if self.axes[4] == -1:
            self.CAROUSEL += 1
        # decrease_carousel_number
        elif self.axes[4] == 1:
            self.CAROUSEL -= 1
        
        # increase_drill_distance
        if self.axes[3] > 0:
            self.DRILL_DISTANCE += 2
        # decrease_drill_distance
        elif self.axes[3] < 0:
            self.DRILL_DISTANCE -= 2

        # increase_drill speed

        if self.axes[5] == 1:
            self.DRILL_SPEED += 10
        if self.axes[5] == -1:
            self.DRILL_SPEED -= 10

        # start_drill
        if self.buttons[4] == 1:
            self.DRILL_STATE = int(self.buttons[4]) 
        elif self.buttons[4] == 0:
            self.DRILL_STATE = int(self.buttons[4]) 
        
        # start_horizontal_auger 
        if self.buttons[6] == 1:
            self.AUGER_STATE = int(self.buttons[6])
        elif self.buttons[6] == 0:
            self.AUGER_STATE = int(self.buttons[6])
        
        # reagent_release
        if self.buttons[7] == 1:
            self.REAGENT = int(self.buttons[7])
        elif self.buttons[7] == 0:
            self.REAGENT = int(self.buttons[7])
            
        
        

        self.CAROUSEL = self.limit_value(self.CAROUSEL, low=1, high=12 )
        self.DRILL_SPEED = self.limit_value(self.DRILL_SPEED, low=-100, high=100)
        #self.DRILL_DISTANCE = self.limit_value(self.CAROUSEL, low=0 , high=100 )


    def set_science_bsx(self):
        pass
    def set_mode(self):

        '''Toggle between arm and arm_IK'''

        if self.buttons[1] == 1:
            self.SET_MODE = 0
            rospy.loginfo("ARM MODE SET")
        # if self.buttons[0] == 1:
        #     self.SET_MODE = 1
        #     rospy.loginfo("SCIENCE MODE SET")
        if self.buttons[2] == 1:
            self.SET_MODE = 2
            rospy.loginfo("ARM INVERSE KINEMATICS SET")


    def limit_value(self, value, low, high):
        if value < low:
            value = low
        if value > high:
            value = high
        return value


    def reset_arm(self):
        self.BASE = 0
        self.SHOULDER = 0
        self.ELBOW = 0
        self.WRIST = 0
        self.GRIPPER = 0


# def publish_array(pub):
#     rospy.loginfo("Base station publishing values")

#     loop_rate = rospy.Rate(10)
#     core = Core()
    
#     while not rospy.is_shutdown():
#         joystick.set_nav_values()
#         joystick.set_mode()

#         core.ld = joystick.LD
#         core.ls = joystick.LS
#         core.rd = joystick.RD
#         core.rs = joystick.RS

#         if joystick.SET_MODE == 0:
#             joystick.set_arm_values()

#             core.base = joystick.BASE
#             core.shoulder = joystick.SHOULDER
#             core.elbow = joystick.ELBOW
#             core.wrist = joystick.WRIST
#             core.gripper = joystick.GRIPPER 
        
#         pub.publish(core)
#         loop_rate.sleep()

# if __name__ == '__main__':
#     joystick = Joystick()
#     pub = rospy.Publisher('atom/core_data', Core, queue_size = 10)
#     rospy.init_node('atom_core_data')
#     publish_array(pub)
#     rospy.spin()






