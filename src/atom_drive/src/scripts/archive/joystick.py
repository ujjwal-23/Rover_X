#! /usr/bin/env python
import rospy
from std_msgs.msg import Int32MultiArray
from atom_drive.msg import Drive
from sensor_msgs.msg import Joy

# This ROS Node converts Joystick inputs from the joy node
# into commands for turtlesim or any other robot

# Receives joystick messages (subscribed to Joy topic)
# then converts the joysick inputs into array commands
# axis 1 aka left stick vertical controls linear speed
# axis 0 aka left stick horizonal controls angular speed

def drive_callback(data):
    
    drive=Drive()
    print(list(data.axes))
    if data.axes[0]>0 and data.axes[1]>0:
        high_speed=(int(abs(data.axes[0]*250))+int(abs(data.axes[1]*250)))/2
        drive.ld=1
        drive.rd=1
        drive.ls=int(high_speed/2)
        drive.rs=int(high_speed)
    elif data.axes[0]<0 and data.axes[1]>0:
        high_speed=(int(abs(data.axes[0]*250))+int(abs(data.axes[1]*250)))/2
        drive.ld=1
        drive.rd=1
        drive.ls=int(high_speed)
        drive.rs=int(high_speed/2)
    elif data.axes[0]>0 and data.axes[1]<0:
        high_speed=(int(abs(data.axes[0]*250))+int(abs(data.axes[1]*250)))/2
        drive.ld=2
        drive.rd=2
        drive.ls=int(high_speed/2)
        drive.rs=int(high_speed)
    elif data.axes[0]<0 and data.axes[1]<0:
        high_speed=(int(abs(data.axes[0]*250))+int(abs(data.axes[1]*250)))/2
        drive.ld=2
        drive.rd=2
        drive.ls=int(high_speed)
        drive.rs=int(high_speed/2)
    
    elif data.axes[1]>0:
        drive.ld=1
        drive.rd=1
        drive.ls=int(abs(data.axes[1]*250))
        drive.rs=int(abs(data.axes[1]*250))
    elif data.axes[1]<0:
        drive.ld=2
        drive.rd=2
        drive.ls=int(abs(data.axes[1]*250))
        drive.rs=int(abs(data.axes[1]*250))
    elif data.axes[0]>0: #left
        drive.ld=2
        drive.rd=1
        drive.ls=int(abs(data.axes[0]*250))
        drive.rs=int(abs(data.axes[0]*250))
    elif data.axes[0]<0: #right
        drive.ld=1
        drive.rd=2
        drive.ls=int(abs(data.axes[0]*250))
        drive.rs=int(abs(data.axes[0]*250))
    pub.publish(drive)

    

# Intializes everything
def start():
    # publishing to "turtle1/cmd_vel" to control turtle1
    global pub
    pub = rospy.Publisher('atom/nav_data', Drive, queue_size = 10)
    # subscribed to joystick inputs on topic "joy"
    rospy.Subscriber('joy', Joy, drive_callback)
    # starts the node
    rospy.init_node('atom_nav_data_node')
    rospy.spin()

if __name__ == '__main__':
    start()
