#! /usr/bin/env python
import rospy
from atom_drive.msg import Middle_list
import time
import imutils
import numpy as np
import pyrealsense2 as rs
from itertools import count 
import cv2
import numpy as np

net = cv2.dnn.readNet('/home/ujjwal/scripts/arrow_detection_harshill/yolov4-custom_best.weights', '/home/ujjwal/scripts/arrow_detection_harshill/yolov4-custom.cfg')

classes = []
with open("/home/ujjwal/scripts/arrow_detection_harshill/arrow.names", "r") as f:
    classes = f.read().splitlines()

#cap = cv2.VideoCapture(2)
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

class DepthCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



        # Start streaming
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    def release(self):
        self.pipeline.stop()

point = (400,300)      
def show_distance(event,x,y,args,params):
    global point
    print(x,y)

if __name__=="__main__":
    dc = DepthCamera()

    cv2.namedWindow("Color frame")
    cv2.setMouseCallback("Color frame",show_distance)
    pub = rospy.Publisher("forward/move",Middle_list,queue_size=20)
    while True:
        ret,depth_frame,color_frame = dc.get_frame()

        height, width, _ = color_frame.shape

        blob = cv2.dnn.blobFromImage(color_frame, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
        core = Middle_list()
        rospy.init_node('arrow_data',anonymous=True)
        net.setInput(blob)
        output_layers_names = net.getUnconnectedOutLayersNames()
        layerOutputs = net.forward(output_layers_names)
        detect = 0
        boxes = []
        confidences = []
        class_ids = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.7:
                    detect = 1
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    # point = [center_x,center_y]
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    confidences.append((float(confidence)))
                    class_ids.append(class_id)


        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

        if len(indexes)>0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i],2))
                color = colors[i]
                cv2.rectangle(color_frame, (x,y), (x+w, y+h), color, 2)
                point = (x+w//2 , y + h//2)
                distance = depth_frame[point[1],point[0]]
        # rospy.init_node('arrow_data',a)
        # core = Middle_list()

                # rospy.init_node('arrow_data',anonymous=True)

                # cv2.imshow('Image', color_frame)
                # key = cv2.waitKey(1)
                # if key==27:
                #     breaknonymous=True)
                # core = Middle_list()
                core.horizontal = point[0]
                core.vertical = point[1]
                core.distance=distance

                if label == "right":
                    core.direction = 1
                elif label == "left":
                    core.direction = 0

                core.detect = detect
                pub.publish(core)
                cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
                cv2.putText(color_frame, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)
                print(class_ids[i] + 1)
        # distance = depth_frame[point[1],point[0]]
        # # rospy.init_node('arrow_data',a)
        # # core = Middle_list()

        # rospy.init_node('arrow_data',anonymous=True)

        # # cv2.imshow('Image', color_frame)
        # # key = cv2.waitKey(1)
        # # if key==27:
        # #     breaknonymous=True)
        # core = Middle_list()
        # core.horizontal = point[0]
        # core.vertical = point[1]
        # if label == "right":
        #     core.direction = 1
        # elif label == "left":
        #     core.direction = 0

        # core.detect = detect
        # pub.publish(core)
        # cv2.putText(color_frame,"{}mm".format(distance),(POINT[0],POINT[1]),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
        else:
            core.detect = 0
            pub.publish(core)
        cv2.imshow("color frame",color_frame)
        key=cv2.waitKey(1)
        if key==27:
            break          
    # dc = DepthCamera()

    # cv2.namedWindow("Color frame")
    # cv2.setMouseCallback("Color frame",show_distance)

    # while True:
    #     ret,depth_frame,color_frame = dc.get_frame()

    #     height, width, _ = color_frame.shape

    #     blob = cv2.dnn.blobFromImage(color_frame, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)

    #     net.setInput(blob)
    #     output_layers_names = net.getUnconnectedOutLayersNames()
    #     layerOutputs = net.forward(output_layers_names)

    #     boxes = []
    #     confidences = []
    #     class_ids = []

    #     for output in layerOutputs:
    #         for detection in output:
    #             scores = detection[5:]
    #             class_id = np.argmax(scores)
    #             confidence = scores[class_id]
    #             if confidence > 0.2:
    #                 center_x = int(detection[0]*width)
    #                 center_y = int(detection[1]*height)
    #                 # point = [center_x,center_y]
    #                 w = int(detection[2]*width)
    #                 h = int(detection[3]*height)

    #                 x = int(center_x - w/2)
    #                 y = int(center_y - h/2)

    #                 boxes.append([x, y, w, h])
    #                 confidences.append((float(confidence)))
    #                 class_ids.append(class_id)


    #     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

    #     if len(indexes)>0:
    #         for i in indexes.flatten():
    #             x, y, w, h = boxes[i]
    #             label = str(classes[class_ids[i]])
    #             confidence = str(round(confidences[i],2))
    #             color = colors[i]
    #             cv2.rectangle(color_frame, (x,y), (x+w, y+h), color, 2)
    #             point = (x+w//2 , y + h//2)
    #             cv2.putText(color_frame, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)
    #             print(class_ids[i] + 1)
    #     distance = depth_frame[point[1],point[0]]
    #     rospy.init_node('arrow_data',anonymous=True)
    #     core = Middle_list()



    #     cv2.imshow('Image', color_frame)
    #     # key = cv2.waitKey(1)
    #     # if key==27:
    #     #     breaknonymous=True)
    #     core = Middle_list()
    #     core.horizontal = point[0]
    #     core.vertical = point[1]
    #     if label == "right":
    #         core.direction = 1
    #     elif label == "left":
    #         core.direction = 0



    #     cv2.imshow('Image', color_frame)
        # key = cv2.waitKey(1)
        # if key==27:
        #     break