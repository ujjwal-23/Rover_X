#! /usr/bin/env python
import rospy
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Joy
from atom_drive.msg import Arm
from joystick3 import Joystick


def publish_values_joy(pub):
    
    rospy.loginfo("Base station publishing  arm values via Joystick")

    loop_rate = rospy.Rate(10)
    arm = Arm()
    
    while not rospy.is_shutdown():
        # if len(joystick.axes)  > 6:
        #     rospy.logfatal("Terminating....... \n Joystick set to XInput mode configure it for DInput mode")
        #     return 0
        joystick.set_mode()
        joystick.set_arm_values()

        if joystick.SET_MODE == 0:
            rospy.loginfo_once("Normal_mode")
            arm.base_speed = joystick.BASE_SPEED
            arm.base_dir = joystick.BASE_DIR
            arm.shoulder_dir = joystick.SHOULDER_DIR
            arm.shoulder_speed = joystick.SHOULDER_SPEED
            arm.elbow_dir = joystick.ELBOW_DIR
            arm.elbow_speed = joystick.ELBOW_SPEED
            arm.yaw_speed = joystick.YAW_SPEED
            arm.yaw_dir = joystick.YAW_DIR
            arm.pitch_speed = joystick.PITCH_SPEED
            arm.pitch_dir = joystick.PITCH_DIR
            arm.roll_speed = joystick.ROLL_SPEED
            arm.roll_dir = joystick.ROLL_DIR
            arm.end_eff_speed = joystick.END_EFF_SPEED
            arm.end_eff_dir = joystick.END_EFF_DIR

        elif joystick.SET_MODE == 1:
            rospy.loginfo_once("Precision_mode")
            arm.base_speed = int(joystick.BASE_SPEED/2)
            arm.base_dir = joystick.BASE_DIR
            arm.shoulder_dir =joystick.SHOULDER_DIR
            arm.shoulder_speed = int(joystick.SHOULDER_SPEED/2)
            arm.elbow_dir = joystick.ELBOW_DIR
            arm.elbow_speed = int(joystick.ELBOW_SPEED/2)
            arm.yaw_speed = int(joystick.YAW_SPEED/2)
            arm.yaw_dir = joystick.YAW_DIR
            arm.pitch_speed = joystick.PITCH_SPEED
            arm.pitch_dir = joystick.PITCH_DIR
            arm.roll_speed = joystick.ROLL_SPEED
            arm.roll_dir = joystick.ROLL_DIR
            arm.end_eff_speed = int(joystick.END_EFF_SPEED/2)
            arm.end_eff_dir = joystick.END_EFF_DIR



        pub.publish(arm)
        loop_rate.sleep()

############## This function will be defined in the other file in some other class ############
    

if __name__ == '__main__':

    rospy.init_node('atom_arm_data')
    joystick = Joystick()
    pub = rospy.Publisher('atom/arm_data', Arm, queue_size = 10)
    publish_values_joy(pub)
    
    


    
    

