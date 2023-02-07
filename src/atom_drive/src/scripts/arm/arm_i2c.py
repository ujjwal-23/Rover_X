#!/usr/bin/env python
import rospy
import smbus
from atom_drive.msg import Arm
#bus = smbus.SMBus(1)
#address=0x10

def Arm_callback(data_msg):
    rospy.loginfo("Writing data to STM: (%d, %d, %d ,%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)", 
        data_msg.base_speed,data_msg.base_dir,
        data_msg.shoulder_dir,data_msg.shoulder_speed, data_msg.elbow_dir, data_msg.elbow_speed, data_msg.yaw_dir, data_msg.yaw_speed, data_msg.pitch_dir, data_msg.pitch_speed, data_msg.roll_dir, data_msg.roll_speed, data_msg.end_eff_dir, data_msg.end_eff_speed)
    arm=[data_msg.base_dir,data_msg.base_speed,data_msg.shoulder_dir, data_msg.shoulder_speed, data_msg.elbow_dir, data_msg.elbow_speed, data_msg.yaw_dir, data_msg.yaw_speed, data_msg.pitch_dir, data_msg.pitch_speed, data_msg.roll_dir, data_msg.roll_speed, data_msg.end_eff_dir, data_msg.end_eff_speed]
    #bus.write_i2c_block_data(address,0,arm)
    
    
rospy.init_node('arm_subscriber_node', anonymous=True)

rospy.Subscriber("atom/arm_data", Arm, Arm_callback)

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()

