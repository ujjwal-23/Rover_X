#!/usr/bin/env python
#import smbus
from distutils import core
import rospy
from atom_drive.msg import Science_bsx
#bus0 = smbus.SMBus(1)


address0 = 0x10


def science_callback(science_msg):
    rospy.loginfo_once("Writing Values to the STM1")
    # rospy.loginfo("new drive data received: (%d, %d, %d ,%d)", 
    #     core_msg.ld,core_msg.ls,
    #     core_msg.rd,core_msg.rs)

    data = [science_msg.ld, 
            science_msg.ls, 
            science_msg.rd,  
            science_msg.rs, 
            science_msg.raman_direction_v, 
            science_msg.raman_speed_v, 
            science_msg.raman_direction_h, 
            science_msg.raman_speed_h, 
            science_msg.drill_direction, 
            science_msg.drill_speed ,
            science_msg.auger_direction, 
            science_msg.h_auger_direction,
            science_msg.carousel_direction,
            science_msg.carousel_speed,
            science_msg.reagent_direction,
            science_msg.servo]

    print("MOTION array to STM1: ", data)
    #bus0.write_i2c_block_data(address0, 0 , data)


rospy.init_node('science_i2c_node', anonymous=True)

rospy.Subscriber("/atom/science_data", Science_bsx, science_callback)

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()
