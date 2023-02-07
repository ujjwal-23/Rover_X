#! /usr/bin/env python
import rospy 
from std_msgs.msg import Float32
from atom_drive.msg import Middle_list
w=0
def subscriber():
    rospy.init_node('log_data',anonymous=True)
    rospy.Subscriber("cardinal_dir",Float32,callback)
    rospy.spin()

def callback(data):
    global x 

    x = data.data
    if w ==1:
        fs = open("data.txt","w")
        if x>315 or x <= 45
            fs.write("direction" + 'north' +"\n")
            fs.close()

        elif x>225 and x <= 315
            fs.write("direction" + "east" +"\n")
            fs.close()

        elif x>135 and x <= 225
            fs.write("direction" + "south" +"\n")
            fs.close()

        elif x>45 and x <= 135
            fs.write("direction" + "west" +"\n")
            fs.close()

def subscriber2():
    rospy.init_node("coordinates",anonymous=True)
    rospy.Subscriber("coordinates",NavSatFix,callback2)
    rospy.spin()

def callback2(data):
    global y,z
    y = data.x
    z = data.y

    if w ==1:
        fs = open("data.txt","w")
        fs.write("coordinates:" + y + "  " + z +"\n")
        fs.close()

def subscriber3():
    rospy.init_node("confimation",anonymous=True)
    rospy.Subscriber("confirmation",Float32,callback3)
    rospy.spin() 

def callback3(data):
    global w
    w = data.confirmation

if __name__=="__main__":
    subscriber()
    subscriber2()
    subscriber3()