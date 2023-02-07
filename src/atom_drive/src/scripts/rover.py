#!/usr/bin/env python
import smbus
from distutils import core
import rospy
from atom_drive.msg import Core
# bus0 = smbus.SMBus(0)
# bus1 = smbus.SMBus(1)

# address0 = 0x10
# address1 = 0x11


def core_callback(core_msg):
    rospy.loginfo_once("Writing Values to the STM1 and STM2 ")
    # rospy.loginfo("new drive data received: (%d, %d, %d ,%d)", 
    #     core_msg.ld,core_msg.ls,
    #     core_msg.rd,core_msg.rs)
    motion=[core_msg.ld, core_msg.ls, core_msg.rd, core_msg.rs]
    arm = [core_msg.base, core_msg.shoulder, core_msg.elbow, core_msg.wrist, core_msg.gripper]

    print("MOTION array to STM1: ", motion)
    # bus0.write_i2c_block_data(address0, 0 , motion)

    print("ARM array to STM2: ", arm)
    # bus1.write_i2c_block_data(address1, 0, arm)

    
rospy.init_node('iot_sensor_subscriber_node', anonymous=True)

rospy.Subscriber("atom/core_data", Core, core_callback)

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()
