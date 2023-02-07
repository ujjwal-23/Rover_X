#!/usr/bin/env python
import rospy
import smbus
from atom_drive.msg import Drive
bus = smbus.SMBus(1)
address=0x10

def Drive_callback(data_msg):
    rospy.loginfo("new drive data received: (%d, %d, %d ,%d)", 
        data_msg.ld,data_msg.ls,
        data_msg.rd,data_msg.rs)
    motion=[data_msg.ld, data_msg.ls, data_msg.rd, data_msg.rs]
    bus.write_i2c_block_data(address,0,motion)

    print(motion)
    
    
rospy.init_node('nav_subscriber_node', anonymous=True)

rospy.Subscriber("atom/nav_data", Drive, Drive_callback)

# spin() simply keeps python from exiting until this node is stopped
rospy.spin()

