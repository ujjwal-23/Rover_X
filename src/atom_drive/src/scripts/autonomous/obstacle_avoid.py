#! /usr/bin/env python

import rospy
from atom_drive.msg import Drive
import cv2
import numpy as np

for i in range (320,0,-1):
    if obstacle[0][i][1]==255 and obstacle[0][i][2]==255:
        count += 1
        value = value+i


for j in range (320,640):
    if obstacle[0][j][1]==255 and obstacle[0][j][2]==255:
        count2 += 1
        value2 = value2+j

value = value/count
value2 = value2/count2
if value<value2:
    if value-320 >100:
        move left diagnol

else:
    if value2 - 320>100:
        move right diagnol 

    else:
        move straight


if count == count2 ==0:
    call node to find other paths

value = 0
value2 = 0

##loop back into with original/reset values of count and count2 at 0 