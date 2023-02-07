#!/usr/bin/env python
import smbus
import rospy
from PyQt5 import QtWidgets,uic
from atom_drive.msg import Science


def science_callback(science_msg):
    global call
    science = Science()
    rospy.loginfo_once("Displaying Values to the STM_VIEWER ")
    motion=[science_msg.ld, science_msg.ls, science_msg.rd, science_msg.rs]
    science = [science_msg.drill_distance, science_msg.drill_state, science_msg.auger_state, science_msg.carousel, science_msg.reagent, science_msg.drill_speed]

    call.ld.display(motion[0])
    call.ls.display(motion[1])
    call.rd.display(motion[2])
    call.rs.display(motion[3])

    call.drill_distance.display(science[0])
    call.drill_state.display(science[1])
    call.auger_state.display(science[2])
    call.carousel.display(science[3])
    call.reagent.display(science[4])
    call.drill_speed.display(science[5])
 

    if science_msg.mode == 0:
        call.mode.setText("ARM MANUAL")
    elif science_msg.mode == 1:
        call.mode.setText("SCIENCE")
    elif science_msg.mode == 2:
        call.mode.setText("ARM INVERSE KINEMATICS")
    elif science_msg.mode == 3:
        call.mode.setText("KIDS MODE")



app=QtWidgets.QApplication([])
call=uic.loadUi("/home/devanshu/drive_ws/src/atom_drive/src/scripts/stm_array_science.ui")
rospy.init_node('display_STM_science', anonymous=True)
rospy.Subscriber("atom/science_data", Science, science_callback)
call.show()
app.exec_()



