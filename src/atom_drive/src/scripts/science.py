#! /usr/bin/env python
import rospy
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Joy
from atom_drive.msg import Science
from joystick1 import Joystick


def publish_values_science(pub):
    rospy.loginfo("Base station publishing science values via Joystick")

    loop_rate = rospy.Rate(5)
    science = Science()
    
    
    while not rospy.is_shutdown():
        joystick.set_nav_values()
        joystick.set_science_values()
        science.mode = joystick.SET_MODE

        science.ld = joystick.LD
        science.ls = joystick.LS
        science.rd = joystick.RD
        science.rs = joystick.RS
        science.drill_distance = joystick.DRILL_DISTANCE
        science.drill_state = joystick.DRILL_STATE
        science.auger_state = joystick.AUGER_STATE
        science.carousel = joystick.CAROUSEL
        science.reagent = joystick.REAGENT
        science.drill_speed = joystick.DRILL_SPEED
        
        
        pub.publish(science)
        loop_rate.sleep()
                                                                                     

if __name__ == '__main__':

    rospy.init_node('atom_science_data')
    joystick = Joystick()
    pub = rospy.Publisher('atom/science_data', Science, queue_size = 10)
    publish_values_science(pub)
   
    
    


    
    

