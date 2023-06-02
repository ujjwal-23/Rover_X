#! /usr/bin/env python
import rospy
from atom_drive.msg import Drive
from sensor_msgs.msg import Imu 
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import MagneticField
import math
a=12.9702994
b=79.1561988
c=0
x=0
y=0
z=0
compass = 0


def subscriber():
    
    rospy.Subscriber("phone1/android/magnetic_field", MagneticField, callback,queue_size=1)


def subscriber2():
    rospy.Subscriber("/fix",NavSatFix,callback2)


def d_forward(pub,core,rate):
    core.ld = 1
    core.rd = 1
    core.ls = 120
    core.rs = 120

    pub.publish(core)
    rate.sleep

def d_diagnol_r(pub,core,rate):
    core.ld = 1
    core.rd = 1
    core.ls = 255
    core.rs = 120

    pub.publish(core)
    rate.sleep

def d_diagnol_l(pub,core,rate):
    core.ld = 1
    core.rd = 1
    core.ls = 120
    core.rs = 255

    pub.publish(core)
    rate.sleep

def t_right(pub,core,rate):
    core.ld = 1
    core.rd = 2
    core.ls = 120
    core.rs = 120

    pub.publish(core)
    rate.sleep 


def t_left(pub,core,rate):
    core.ld = 2
    core.rd = 1
    core.ls = 120
    core.rs = 120

    pub.publish(core)
    rate.sleep 

def callback(data):
    global x
    global y
    global z
    global compass
    x = data.magnetic_field.x
    y = data.magnetic_field.y
    z = data.magnetic_field.z
    compass = round(math.atan2(y,x)*180/math.pi,1)
    compass = (compass-90)
    if(compass<0):
        compass += 360

def callback2(data):
    global a
    global b
    global c
    a = data.latitude
    b = data.longitude
    c = math.atan((m-a)/(n-b))

def publisher(pub):
    global m
    global n

    core = Drive()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        while abs(a-m)> 0 or abs(b-n)>0:
            d_forward(pub,core,rate)
            if abs(c-compass)>5:
                while abs(c-compass)>5:
                    t_right(pub,core,rate)
if __name__=='__main__':
    global m
    global n
    m = 12.9682655
    n = 79.1558873
    pub = rospy.Publisher('calibrate/auto',Drive,queue_size=20)
    rospy.init_node('go_to_point',anonymous=True)
    subscriber()
    # subscriber2()
    publisher(pub)
















# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive
# from sensor_msgs.msg import Imu 
# from sensor_msgs.msg import NavSatFix
# from sensor_msgs.msg import MagneticField
# import math


# def subscriber():
    
#     rospy.Subscriber("phone1/android/magnetic_field", MagneticField, callback,queue_size=1)


# def subscriber2():
#     rospy.Subscriber("/fix",NavSatFix,callback2)


# def d_forward(pub,core,rate):
#     core.ld = 1
#     core.rd = 1
#     core.ls = 120
#     core.rs = 120

#     pub.publish(core)
#     rate.sleep

# def d_diagnol_r(pub,core,rate):
#     core.ld = 1
#     core.rd = 1
#     core.ls = 255
#     core.rs = 120

#     pub.publish(core)
#     rate.sleep

# def d_diagnol_l(pub,core,rate):
#     core.ld = 1
#     core.rd = 1
#     core.ls = 120
#     core.rs = 255

#     pub.publish(core)
#     rate.sleep

# def t_right(pub,core,rate):
#     core.ld = 1
#     core.rd = 2
#     core.ls = 120
#     core.rs = 120

#     pub.publish(core)
#     rate.sleep 


# def t_left(pub,core,rate):
#     core.ld = 2
#     core.rd = 1
#     core.ls = 120
#     core.rs = 120

#     pub.publish(core)
#     rate.sleep 

# def callback(data):
#     global x
#     global y
#     global z
#     global compass
#     x = data.magnetic_field.x
#     y = data.magnetic_field.y
#     z = data.magnetic_field.z
#     compass = round(math.atan2(y,x)*180/math.pi,1)
#     compass = (compass-90)
#     if(compass<0):
#         compass += 360

# def callback2(data):
#     global a
#     global b
#     global c
#     a = data.latitude
#     b = data.longitude
#     c = math.atan((m-a)/(n-b))

# def publisher():

#     core = Drive()
#     rate = rospy.Rate(10)
#     while not rospy.is_shutdown():
#         while abs(a-m)> 0.00001 or abs(b-n)>0.00001:
#             d_forward(pub,core,rate)
#             if abs(c-compass)>5:
#                 while abs(c-compass)>5:
#                     t_right(pub,core,rate)
# if __name__=='__main__':
#     m = "target_x"
#     n = "target_y"
#     pub = rospy.Publisher('calibrate/auto',Drive,queue_size=20)
#     rospy.init_node('go_to_point',anonymous=True)
#     subscriber()
#     subscriber2()
#     publisher(pub)













































# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive
# from sensor_msgs.msg import Imu 
# from sensor_msgs.msg import NavSatFix
# import math


# def subscriber():
#     rospy.init_node('go_to_point',anonymous=True)
#     rospy.Subscriber("phone1/android/magnetic_field", MagneticField, self.callback,queue_size=1)


# def subscriber2():
#     rospy.Subscriber("/fix",NavSatFix,callback2)


# def d_forward(pub,core,rate):
#     core.ld = 1
#     core.rd = 1
#     core.ls = 120
#     core.rs = 120

#     pub.publish(core)
#     rate.sleep

# def d_diagnol_r(pub,core,rate):
#     core.ld = 1
#     core.rd = 1
#     core.ls = 255
#     core.rs = 120

#     pub.publish(core)
#     rate.sleep

# def d_diagnol_l(pub,core,rate):
#     core.ld = 1
#     core.rd = 1
#     core.ls = 120
#     core.rs = 255

#     pub.publish(core)
#     rate.sleep

# def t_right(pub,core,rate):
#     core.ld = 1
#     core.rd = 2
#     core.ls = 120
#     core.rs = 120

#     pub.publish(core)
#     rate.sleep 


# def t_left(pub,core,rate):
#     core.ld = 2
#     core.rd = 1
#     core.ls = 120
#     core.rs = 120

#     pub.publish(core)
#     rate.sleep 

# def callback(data):
#     global x
#     global y
#     global z
#     global compass
#     x = data.magnetic_field.x
#     y = data.magnetic_field.y
#     z = data.magnetic_field.z
#     compass = round(math.atan2(y,x)*180/math.pi,1)
#     compass = (compass-90)
#     if(compass<0):
#         compass += 360

# def callback2(data):
#     global a
#     global b
#     global c
#     a = data.latitude
#     b = data.longitude
#     c = math.atan((m-a)/(n-b))

# def publisher():

#     core = Drive()
#     rate = rospy.Rate(10)
#     while not rospy.is_shutdown():
#         while abs(a-m)> 0.00001 or abs(b-n)>0.00001:
#             d_forward(pub,core,rate)
#             if abs(c-compass)>5:
#                 while abs(c-compass)>5:
#                     t_right(pub,core,rate)

#                 # if c - compass > 5:
#                 #     while abs(c-compass)>5:
#                 #         t_left(pub,core,rate)

#                 # if compass - c < -5:
#                 #     while abs(c-compass)>5:
#                 #         t_right(pub,core,rate)

# if __name__=='__main__':
#     m = "target_x"
#     n = "target_y"
#     pub = rospy.Publisher('calibrate/auto',Drive,queue_size=20)
#     subscriber()
#     subscriber2()
#     publisher(pub)