#!/usr/bin/env python
#import smbus
from statistics import mode
import rospy
from PyQt5 import uic, QtWidgets
from atom_drive.msg import Science_bsx
import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(2)
        cap2 = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            ret2, frame2 = cap2.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(750,750,Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            if ret2:
                rgbImage2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                h2, w2, ch2 = rgbImage2.shape
                bytesPerLine2 = ch2 * w2
                convertToQtFormat2 = QImage(rgbImage2.data, w2, h2, bytesPerLine2, QImage.Format_RGB888)
                p2 = convertToQtFormat2.scaled(750,750,Qt.KeepAspectRatio)
                self.changePixmap.emit(p2)
@pyqtSlot(QImage)
def setImage(image):
    call.stream.setPixmap(QPixmap.fromImage(image))
def setImage2(image):
	call.stream2.setPixmap(QPixmap.fromImage(image))
def set_raman():
    pixmap = QPixmap('/home/ujjwal/drive_ws/src/atom_drive/src/scripts/Bsx/raman.png')
    call.raman.setPixmap(pixmap)
    call.raman.setScaledContents(True)
    #call.raman.setStyleSheet("background-image: url(/home/devanshu/drive_ws/src/atom_drive/src/scripts/Bsx/raman.png);")

def remove_raman():
    pixmap = QPixmap('')
    call.raman.setPixmap(pixmap)
    call.raman.setScaledContents(True)

def science_callback(science_msg):
    global call
    # science = Science_bsx()

    rospy.loginfo_once("Displaying Values to the STM_VIEWER ")
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
            science_msg.reagent_direction]

    call.ld.display(data[0])
    call.ls.display(data[1])
    call.rd.display(data[2])
    call.rs.display(data[3])

    call.raman_dir_v.display(data[4])
    call.raman_speed_v.display(data[5])
    call.raman_dir_h.display(data[6])
    call.raman_speed_h.display(data[7])
    call.drill_dir.display(data[8])
    call.drill_speed.display(data[9])
    call.auger_dir.display(data[10])
    call.h_auger_dir.display(data[11])
    call.carousel_dir.display(data[12])
    call.reagent.display(data[14])
 

    if science_msg.mode == 0:
        call.mode.setText("Raman Spectrometer")
        call.label_raman.setStyleSheet("background-color: green; color:white") #rgb(108,188,70)
        call.label_drill.setStyleSheet("color:white; border: 1px solid grey;")
        call.label_sample.setStyleSheet("color:white; border: 1px solid grey;")
    if science_msg.mode == 1:
        call.mode.setText("Drill System")
        call.label_drill.setStyleSheet("background-color: green; color:white")
        call.label_raman.setStyleSheet("color:white; border: 1px solid grey;")
        call.label_sample.setStyleSheet("color:white; border: 1px solid grey;")
        
    if science_msg.mode == 2:
        call.mode.setText("Sampling System")
        call.label_sample.setStyleSheet("background-color: green; color:white")
        call.label_raman.setStyleSheet("color:white; border: 1px solid grey;")
        call.label_drill.setStyleSheet("color:white; border: 1px solid grey;")
    
    if science_msg.mode == 3:
        call.mode.setText("KIDS MODE :)")

raman_display_on = False
def raman():
    global raman_display_on
    if raman_display_on:
        remove_raman()
        raman_display_on = False
    else:
        set_raman()
        raman_display_on = True


#th = Thread()
#th.changePixmap.connect(setImage)
#th.start()

#th2 = Thread()
#th2.changePixmap.connect(setImage2)
#th2.start()

app=QtWidgets.QApplication([])
call=uic.loadUi("/home/ujjwal/drive_ws/src/atom_drive/src/scripts/irc_new_worst.ui")
rospy.init_node('display_STM_science_Bsx', anonymous=True)
rospy.Subscriber("atom/science_data", Science_bsx, science_callback)
call.bt_raman.clicked.connect(raman)
# call.bt_camera.clicked.connect(th.start)
# call.bt_camera.clicked.connect(th.wait)
call.show()
app.exec_()








"""

#!/usr/bin/env python
#import smbus
from statistics import mode
import rospy
from PyQt5 import uic, QtWidgets
from atom_drive.msg import Science_bsx
import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(450,450,Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

@pyqtSlot(QImage)
def setImage(image):
    call.stream.setPixmap(QPixmap.fromImage(image))

def set_raman():
    pixmap = QPixmap('/home/ujjwal/drive_ws/src/atom_drive/src/scripts/Bsx/raman.png')
    call.raman.setPixmap(pixmap)
    call.raman.setScaledContents(True)
    #call.raman.setStyleSheet("background-image: url(/home/devanshu/drive_ws/src/atom_drive/src/scripts/Bsx/raman.png);")

def remove_raman():
    pixmap = QPixmap('')
    call.raman.setPixmap(pixmap)
    call.raman.setScaledContents(True)

def science_callback(science_msg):
    global call
    # science = Science_bsx()

    rospy.loginfo_once("Displaying Values to the STM_VIEWER ")
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
            science_msg.reagent_direction]

    call.ld.display(data[0])
    call.ls.display(data[1])
    call.rd.display(data[2])
    call.rs.display(data[3])

    call.raman_dir_v.display(data[4])
    call.raman_speed_v.display(data[5])
    call.raman_dir_h.display(data[6])
    call.raman_speed_h.display(data[7])
    call.drill_dir.display(data[8])
    call.drill_speed.display(data[9])
    call.auger_dir.display(data[10])
    call.h_auger_dir.display(data[11])
    call.carousel_dir.display(data[12])
    call.reagent.display(data[14])
 

    if science_msg.mode == 0:
        call.mode.setText("Raman Spectrometer")
        call.label_raman.setStyleSheet("background-color: green; color:white") #rgb(108,188,70)
        call.label_drill.setStyleSheet("color:white; border: 1px solid grey;")
        call.label_sample.setStyleSheet("color:white; border: 1px solid grey;")
    if science_msg.mode == 1:
        call.mode.setText("Drill System")
        call.label_drill.setStyleSheet("background-color: green; color:white")
        call.label_raman.setStyleSheet("color:white; border: 1px solid grey;")
        call.label_sample.setStyleSheet("color:white; border: 1px solid grey;")
        
    if science_msg.mode == 2:
        call.mode.setText("Sampling System")
        call.label_sample.setStyleSheet("background-color: green; color:white")
        call.label_raman.setStyleSheet("color:white; border: 1px solid grey;")
        call.label_drill.setStyleSheet("color:white; border: 1px solid grey;")
    
    if science_msg.mode == 3:
        call.mode.setText("KIDS MODE :)")

raman_display_on = False
def raman():
    global raman_display_on
    if raman_display_on:
        remove_raman()
        raman_display_on = False
    else:
        set_raman()
        raman_display_on = True


th = Thread()
th.changePixmap.connect(setImage)
th.start()

app=QtWidgets.QApplication([])
call=uic.loadUi("/home/ujjwal/drive_ws/src/atom_drive/src/scripts/irc_new_worst.ui")
rospy.init_node('display_STM_science_Bsx', anonymous=True)
rospy.Subscriber("atom/science_data", Science_bsx, science_callback)
call.bt_raman.clicked.connect(raman)
# call.bt_camera.clicked.connect(th.start)
# call.bt_camera.clicked.connect(th.wait)
call.show()
app.exec_()


"""
