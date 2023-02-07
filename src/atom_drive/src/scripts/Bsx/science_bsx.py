#! /usr/bin/env python
import rospy
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Joy
from atom_drive.msg import Science_bsx
from joystick2 import Joystick


def publish_values_science(pub):
    rospy.loginfo("Base station publishing science values via Joystick")

    loop_rate = rospy.Rate(10)
    science = Science_bsx()
    
    
    while not rospy.is_shutdown():
#    	 if len(joystick.axes)  > 6:
#             rospy.logwarn("Terminating....... \n Joystick set to XInput mode configure it for DInput mode")
#             return 0
        joystick.set_nav_values()
        joystick.set_mode()
        joystick.set_science_values()
        
        if joystick.SET_MODE == 3:
            science.mode = joystick.SET_MODE
            science.ld = joystick.LD
            science.ls = int(joystick.LS/4)
            science.rd = joystick.RD
            science.rs = int(joystick.RS/4)
            science.raman_direction_h = joystick.RAMAN_DIRECTION_H
            science.raman_speed_h = int(joystick.RAMAN_SPEED_H)
            science.raman_direction_v = joystick.RAMAN_DIRECTION_V
            science.raman_speed_v = int(joystick.RAMAN_SPEED_V/4)
            science.drill_direction = joystick.DRILL_DIRECTION
            science.drill_speed = int(joystick.DRILL_SPEED/4)
            science.auger_direction = joystick.AUGER_DIRECTION
            science.h_auger_direction = joystick.H_AUGER_DIRECTION
            science.carousel_direction = joystick.CAROUSEL_DIRECTION
            science.carousel_speed = joystick.CAROUSEL_SPEED
            science.reagent_direction = joystick.REAGENT_DIRECTION
            science.servo = joystick.SERVO

        else: 
            science.mode = joystick.SET_MODE
            science.ld = joystick.LD
            science.ls = joystick.LS
            science.rd = joystick.RD
            science.rs = joystick.RS
            science.raman_direction_h = joystick.RAMAN_DIRECTION_H
            science.raman_speed_h = joystick.RAMAN_SPEED_H
            science.raman_direction_v = joystick.RAMAN_DIRECTION_V
            science.raman_speed_v = joystick.RAMAN_SPEED_V
            science.drill_direction = joystick.DRILL_DIRECTION
            science.drill_speed = joystick.DRILL_SPEED
            science.auger_direction = joystick.AUGER_DIRECTION
            science.h_auger_direction = joystick.H_AUGER_DIRECTION
            science.carousel_direction = joystick.CAROUSEL_DIRECTION
            science.carousel_speed = joystick.CAROUSEL_SPEED
            science.reagent_direction = joystick.REAGENT_DIRECTION
            science.servo = joystick.SERVO
          
        pub.publish(science)
        loop_rate.sleep()
                                                                                     

if __name__ == '__main__':

    rospy.init_node('atom_science_data_bsx')
    joystick = Joystick()
    pub = rospy.Publisher('atom/science_data', Science_bsx, queue_size = 20)
    publish_values_science(pub)
   
    
    


    
    

