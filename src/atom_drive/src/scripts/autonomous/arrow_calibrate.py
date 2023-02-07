#! /usr/bin/env python
import rospy

import cv2
import pyrealsense2
#from realsense_depth import *
import numpy as np
import pyrealsense2 as rs
from atom_drive.msg import Middle_list   #list of two int32
from atom_drive.msg import Drive
from std_msgs.msg import Float32
# from sensor_msgs.msg import Imu

x = 0
y = 0
z = 0 
#arrow_point = [0 , 0]
# class DepthCamera:
#     def __init__(self):
#         self.pipeline = rs.pipeline()
#         config = rs.config()
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#         self.pipeline.start(config)

#     def get_frame(self):
#         frames = self.pipeline.wait_for_frames()
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()

#         depth_image = np.asanyarray(depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())
#         if not depth_frame or not color_frame:
#             return False, None, None
#         return True, depth_image, color_image

#     def release(self):
#         self.pipeline.stop()

# def show_distance(event, x, y, args, params):
#     global point
#     point = (x, y)



#cv2.namedWindow("Color frame")
#cv2.setMouseCallback("Color frame", show_distance)

def subscriber():
    rospy.init_node('auto_calibrate',anonymous=True)
    rospy.Subscriber('forward/move',Middle_list,callback)
    # rospy.Subscriber('arrow/middle',Middle_list,callback)

# def subscriber2():
#     rospy.Subscriber('arrow/distance',Float32,callback)
 
def callback(data):
    # global arrow_point
    # arrow_point = Middle_list()
    # arrow_point.horizontal = data.horizontal
    # arrow_point.vertical = data.vertical  
    # arrow_point.distance = data.distance
    global x
    global y
    global z
    x = data.horizontal
    y = data.vertical
    z = data.distance

def publisher(pub):
    # dc = DepthCamera()

    # ret, depth_frame, color_frame = dc.get_frame()
    # point = (400,300)
    # cv2.circle(color_frame, point, 4, (0, 0, 255))
    # distance = depth_frame[point[1], point[0]]

    # cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    # rate=rospy.Rate(10)
    # core = Drive()
    arrow_point = Middle_list()
    core = Drive()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # ret, depth_frame, color_frame = dc.get_frame()
        # if ret == True:
        arrow_point.horizontal = x
        arrow_point.vertical = y
        arrow_point.distance = z
        if arrow_point.horizontal > 330:
            core.ld = 2
            core.ls = 120
            core.rd = 1
            core.rs = 120

            pub.publish(core)
            rate.sleep()
        elif arrow_point.horizontal < 160:
            core.ld = 1
            core.ls = 120
            core.rd = 2
            core.rs = 120

            pub.publish(core)
            rate.sleep()

        else:
            if arrow_point.distance > 200:
                core.ld = 1
                core.ls = 150
                core.rd = 1
                core.rs = 150

                pub.publish(core)
                rate.sleep()

            else :
                core.ld = 0
                core.ls = 0
                core.rd = 0 
                core.rs = 0

                pub.publish(core)
                rate.sleep()

#when no arrow is detected then the rover should publish 0,0,0,0 to the rover and if after a given time interval arrow is not detected then go for expanding 
#spiral search to find the arrow . 
#in the arrow detection file itself publish if the arrow is bieng detcted or not

# use if a && if b 
#     or go for 
#     if a:
#         if b:
    # prior one is better performance in ros -reason unknown


if __name__ == '__main__':




    # while True:
    #     ret, depth_frame, color_frame = dc.get_frame()

    #     cv2.circle(color_frame, point, 4, (0, 0, 255))
    #     distance = depth_frame[point[1], point[0]]

    #     cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    #     cv2.imshow("depth frame", depth_frame)
    #     cv2.imshow("Color frame", color_frame)
    #     key = cv2.waitKey(1)
    #     if key == 27:
    #         break

    pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
    subscriber()
    publisher(pub)










"""
#! /usr/bin/env python
import rospy

import cv2
import pyrealsense2
#from realsense_depth import *
import numpy as np
import pyrealsense2 as rs
from atom_drive.msg import Middle_list   #list of two int32
from atom_drive.msg import Drive

# class DepthCamera:
#     def __init__(self):
#         self.pipeline = rs.pipeline()
#         config = rs.config()
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#         self.pipeline.start(config)

#     def get_frame(self):
#         frames = self.pipeline.wait_for_frames()
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()

#         depth_image = np.asanyarray(depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())
#         if not depth_frame or not color_frame:
#             return False, None, None
#         return True, depth_image, color_image

#     def release(self):
#         self.pipeline.stop()

# def show_distance(event, x, y, args, params):
#     global point
#     point = (x, y)



#cv2.namedWindow("Color frame")
#cv2.setMouseCallback("Color frame", show_distance)

def subscriber():
    rospy.init_node('auto_calibrate',anonymous=True)
    rospy.Subscriber('arrow/middle',Middle_list,callback)
 
def callback(data):
    global arrow_point
    arrow_point = Middle_list()
    arrow_point.horizontal = data.horizontal
    arrow_point.vertical = data.vertical  

def publisher(pub):
    # dc = DepthCamera()

    # ret, depth_frame, color_frame = dc.get_frame()
    # point = (400,300)
    # cv2.circle(color_frame, point, 4, (0, 0, 255))
    # distance = depth_frame[point[1], point[0]]

    # cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    # rate=rospy.Rate(10)
    # core = Drive()
    
    while not rospy.is_shutdown():
        # ret, depth_frame, color_frame = dc.get_frame()
        # if ret == True:
        if arrow_point.horizontal > 430:
            core.ld = 1
            core.ls = 255
            core.rd = 2
            core.rs = 255

            pub.publish(core)
            rate.sleep()
        if arrow_point.horizontal < 330:
            core.ld = 2
            core.ls = 255
            core.rd = 1
            core.rs = 255

            pub.publish(core)
            rate.sleep()

        else:
            core.ld = 2
            core.ls = 255
            core.rd = 2
            core.rs = 255

            pub.publish(core)
            rate.sleep()

if __name__ == '__main__':




    # while True:
    #     ret, depth_frame, color_frame = dc.get_frame()

    #     cv2.circle(color_frame, point, 4, (0, 0, 255))
    #     distance = depth_frame[point[1], point[0]]

    #     cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    #     cv2.imshow("depth frame", depth_frame)
    #     cv2.imshow("Color frame", color_frame)
    #     key = cv2.waitKey(1)
    #     if key == 27:
    #         break

    pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
    subscriber()
    publisher(pub)

"""
