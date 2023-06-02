#! /usr/bin/env python
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import Imu 
from sensor_msgs.msg import MagneticField
from sensor_msgs.msg import NavSatFix


c = 0
d = 0
counter = 0
e = 0
counter2=0
p=0
def subscriber():
    rospy.init_node('callbacks',anonymous=True)
    #it is publsihed one by other nodes if the motors are getting command to move 
    rospy.Subscriber('/stuck',Float32,callback)

def callback(data):
    global a
    a = data.data


def subscriber2():
    rospy.Subscriber('/fix',NavSatFix,callback2)

def callback2(data):
    global x
    global y
    global c
    global e
    global b
    x= data.latitude
    y=data.longitude
    e = e+1
    if abs(x-c)>0.001 or abs(y-d)>0.001:
        c=x
        d=y
        counter = counter + 1


    # if e > 100 and counter <2:
    #     #publish b as 0
    if e%100==1:
        if abs(x+y - p)<0.001:
            counter2=counter2+1
        else:
            counter2 = 0 
        p=x+y
        
        if counter2>=2:
            b=0


    #use linear acceleration and linear velocity from imu for better data 
    # b=0
    # take a variable outside of the loop and when the callback value changes significantly from it then change it and increase the counter as well , if the counter is increasing then the rover is moving otherwise set b to 0




def publisher(pub):
    rate=rospy.Rate(10)
    core = Float32()
    if a ==1 and b == 0:
        core.data = 1 #needs recovery
        pub.publish(core)
        rate.sleep

        

if __name__=='__main__':
    pub=rospy.Publisher("/moving?",Float32,queue_size=20)
    subscriber()
    subscriber2()
    publisher(pub)


#take difference between depths of two ends of aruco tags to see  if it is aligned with rover or not and write if (while) condition in foraward command which aligns the rover while moving forward by entering into if-while conditions