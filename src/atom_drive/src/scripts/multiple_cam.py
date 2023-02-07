#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys





"""
import cv2 
import imutils
import numpy as np
cap1=cv2.VideoCapture(0)
cap2=cv2.VideoCapture('rtsp://admin:RoverX123@192.168.1.64/1')
cap3=cv2.VideoCapture(2)
cap4=cv2.VideoCapture(3)

while True:
    _1,img1=cap1.read()
    _2,img2=cap2.read()
    _3,img3=cap3.read()
    _4,img4=cap4.read()

    newimg=np.concatenate((img1,imutils.resize(img2,width=854)),1)
    newimg1=np.concatenate((img3,newimg),1)
    finalimg=np.concatenate((imutils,resize(img4,length=660),imutils.resize(newimg1,length=660)),0)

    cv2.imshow("cap",finalimg)
    #cv2.imshow("cap2",img3)
    cv2.waitKey(0)

"""

    
