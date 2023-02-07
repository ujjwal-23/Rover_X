#!/usr/bin/env python
import rospy
#import smbus
from atom_drive.msg import Arm
from atom_drive.msg import Drive
from pythonping import ping 

# pg = ping('192.168.1.2',verbose = True)
ARM = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MOTION = [0, 0, 0, 0]
ARRAY = ARM + MOTION
#bus = smbus.SMBus(1)
#address=0x10
pg = 10
def Arm_callback(arm_msg):
    global ARM
    global MOTION
    global ARRAY

    # rospy.loginfo("Writing data to STM: (%d, %d, %d ,%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)", 
    #     arm_msg.base_speed,arm_msg.base_dir,
    #     arm_msg.shoulder_dir,arm_msg.shoulder_speed, arm_msg.elbow_dir, arm_msg.elbow_speed, arm_msg.yaw_dir, arm_msg.yaw_speed, arm_msg.pitch_dir, arm_msg.pitch_speed, arm_msg.roll_dir, arm_msg.roll_speed, arm_msg.end_eff_dir, arm_msg.end_eff_speed)
    
    ARM=[arm_msg.base_dir,arm_msg.base_speed,arm_msg.shoulder_dir, arm_msg.shoulder_speed, arm_msg.elbow_dir, arm_msg.elbow_speed, arm_msg.yaw_dir, arm_msg.yaw_speed, arm_msg.pitch_dir, arm_msg.pitch_speed, arm_msg.roll_dir, arm_msg.roll_speed, arm_msg.end_eff_dir, arm_msg.end_eff_speed, arm_msg.sol_dir]
    ARRAY = MOTION + ARM
    pg = 10
    #pg = ping('192.168.1.2',verbose = True,timeout = 0.5)  
    pg = ping('192.168.1.2',verbose = True,timeout = 10) 
    if pg.rtt_avg_ms < 500 :
        print(ARRAY)
        #bus.write_i2c_block_data(address,0,AARAY)set_mode

    else:
        ARRAY=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        print(ARRAY)

def Drive_callback(drive_msg):
    global ARM
    global MOTION
    global ARRAY

    MOTION = [drive_msg.ld, drive_msg.ls, drive_msg.rd, drive_msg.rs] 
    pg = 10
    pg = ping('192.168.1.2',verbose = True,timeout=15)  
    ARRAY = ARM + MOTION
    if pg.rtt_avg_ms < 500:
        #bus.write_i2c_block_data(address,0,ARRAY)
        print(ARRAY)
    else:
        ARRAY=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        print(ARRAY)

rospy.init_node('arm_subscriber_node', anonymous=True)

rospy.Subscriber("atom/arm_data", Arm, Arm_callback)
rospy.Subscriber("atom/nav_data", Drive, Drive_callback )
# spin() simply keeps python from exiting until this node is stopped
rospy.spin()

