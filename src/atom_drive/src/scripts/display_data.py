#!/usr/bin/env python
import smbus
import rospy
from PyQt5 import QtWidgets,uic
from atom_drive.msg import Core


def core_callback(core_msg):
    global call
    rospy.loginfo_once("Displaying Values to the STM_VIEWER ")
    core = Core()
    motion=[core_msg.ld, core_msg.ls, core_msg.rd, core_msg.rs]
    arm = [core_msg.base, core_msg.shoulder, core_msg.elbow, core_msg.wrist, core_msg.gripper]

    call.ld.display(motion[0])
    call.ls.display(motion[1])
    call.rd.display(motion[2])
    call.rs.display(motion[3])

    call.base.display(arm[0])
    call.shoulder.display(arm[1])
    call.elbow.display(arm[2])
    call.pitch.display(arm[3])
    call.grip.display(arm[4])

    if core_msg.mode == 0:
        call.mode.setText("ARM MANUAL")
    elif core_msg.mode == 1:
        call.mode.setText("SCIENCE")
    elif core_msg.mode == 2:
        call.mode.setText("ARM INVERSE KINEMATICS")



app=QtWidgets.QApplication([])
call=uic.loadUi("/home/devanshu/drive_ws/src/atom_drive/src/scripts/stm_array.ui")
rospy.init_node('display_STM_node', anonymous=True)
rospy.Subscriber("atom/core_data", Core, core_callback)
call.show()
app.exec_()



