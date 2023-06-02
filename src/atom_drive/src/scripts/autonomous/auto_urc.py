#! /usr/bin/env python
import rospy
from atom_drive.msg import Drive

import cv2
#import pyrealsense2
import pyrealsense2 as rs
import numpy as np

safe_path=340

class DepthCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution





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

point = (320,240)      
def show_distance(event,x,y,args,params):
    global point
    print(x,y)


dc = DepthCamera()

cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame",show_distance)



if __name__ == '__main__':
    list = []

    #pub = rospy.Publisher('calibrate/auto', Drive, queue_size=40)
    pub = rospy.Publisher('atom/nav_data', Drive, queue_size=40)
    rospy.init_node('obstacle_avoidance',anonymous=True)
    core = Drive()
    rate = rospy.Rate(10)
    while True:
        ret,depth_frame,color_frame = dc.get_frame()
        cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
        obstacle = color_frame

        distance = depth_frame[point[1],point[0]]
        
        #print(distance)
        
        cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
        cv2.imshow("depth frame",depth_frame)
        cv2.imshow("Color frame",color_frame)
        # obstacle[20][50]  = (0,0,255)


        counter =1
        counter2=1
        counter3=1
        value = 340
        value2 = 340
       
        if (distance > 600):
            for j in range(639,0,-1):
                cal = 0
                for i in range(479,0,-1):
                    if depth_frame[i,j] - depth_frame[i-1,j]> 5:
                        cal = cal + 1
                        obstacle[i][j] = (0,255,0)

                    else:
                        obstacle[i][j] = (0,0,255)
                if cal > 350:
                    obstacle[0][j]=(255,0,0)
                    if j<639 and j>340:
                        counter = counter + 1
                        value = value +1
                    if j<340 and j>40:
                        counter2 = counter2 + 1
                        value2 = value2 +1 
                    if j<380 and j>260:
                        counter3 = counter3+1                  
                else :
                    obstacle[0][j]=(0,255,255)


            value = value//counter
            value2 = value2// counter2

            boolean = 0
            boolean2 = 0

            if counter3>165:
                boolean2=1
                core.ld=1
                core.ls=200
                core.rd=1
                core.ls=200
                pub.publish(core)
                rate.sleep()


            if boolean2 ==0:
                if counter + counter2 < 4:
                    #publish command to start recovery node and command to stop
                    core.ld = 0
                    core.ls = 0
                    core.rd = 0
                    core.rs = 0
                    boolean = 1
                    pub.publish(core)
                    rate.sleep()
                    print("not ok")

                elif counter + counter2 > 550:
                    core.ld = 1
                    core.ls = 100
                    core.rd = 1
                    core.rs = 100
                    boolean = 1
                    pub.publish(core)
                    rate.sleep()



                if boolean == 0:
                    if counter < counter2:
                        if abs(value2-340)> 100:
                            #diagnol right
                            core.ld = 1
                            core.ls = 250
                            core.rd = 1
                            core.rs = 80
                            # print("ok")
                            pub.publish(core)
                            rate.sleep()
                        else:

                            core.ld = 1
                            core.ls = 150
                            core.rd = 1
                            core.rs = 150
                            pub.publish(core)
                            rate.sleep()

                    else:
                        if abs(value-340)>100:

                            core.ld = 1
                            core.ls = 80
                            core.rd = 1
                            core.rs = 250

                            pub.publish(core)
                            rate.sleep()

                        else:

                            core.ld = 1
                            core.ls = 150
                            core.rd = 1
                            core.rs = 150
                            pub.publish(core)
                            rate.sleep()
        else:
            core.ld=1
            core.ls=0
            core.rd=1
            core.rs=0
            pub.publish(core)
            rate.sleep()
                    

        cv2.imshow("obstacle",obstacle)

        print(list)
        key=cv2.waitKey(1)
        if key==27:
            break






# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=340

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution





#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     #pub = rospy.Publisher('calibrate/auto', Drive, queue_size=40)
#     pub = rospy.Publisher('atom/nav_data', Drive, queue_size=40)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)


#         counter =1
#         counter2=1
#         counter3=1
#         value = 340
#         value2 = 340
       

#         for j in range(639,0,-1):
#             cal = 0
#             for i in range(479,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:
#                     cal = cal + 1
#                     obstacle[i][j] = (0,255,0)

#                 else:
#                     obstacle[i][j] = (0,0,255)
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)
#                 if j<639 and j>340:
#                     counter = counter + 1
#                     value = value +1
#                 if j<340 and j>40:
#                     counter2 = counter2 + 1
#                     value2 = value2 +1 
#                 if j<380 and j>260:
#                     counter3 = counter3+1                  
#             else :
#                 obstacle[0][j]=(0,255,255)

#         # for j in range(0,639):
#         #     cal = 0
#         #     for i in range(0,479):
#         #         if obstacle[i][j][1] == 255:
#         #             cal = cal+1
#         #     if cal > 350:
#         #         obstacle[0][j]=(255,0,0)

#         #     else :
#         #         obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         # counter =1
#         # counter2=1
#         # counter3=1
#         # value = 340
#         # value2 = 340

#         # for i in range(340,639):
#         #     if obstacle[0][i][0]==255 :
#         #         counter = counter +1
#         #         value = value + i #right

#         # for j in range (340,40,-1):
#         #     if obstacle[0][j][0]==255: 
#         #         counter2 = counter2 + 1
#         #         value2 = value2+j   #left
#         # for k in range (260,380):
#         #     if obstacle[0][k][0]==255:
#         #         counter3 = counter3 +1

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight

#         boolean = 0
#         boolean2 = 0

#         if counter3>165:
#             boolean2=1
#             core.ld=1
#             core.ls=200
#             core.rd=1
#             core.ls=200
#             pub.publish(core)
#             rate.sleep()


#         if boolean2 ==0:
#             if counter + counter2 < 4:
#                 #publish command to start recovery node and command to stop
#                 core.ld = 0
#                 core.ls = 0
#                 core.rd = 0
#                 core.rs = 0
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()
#                 print("not ok")

#             elif counter + counter2 > 550:
#                 core.ld = 1
#                 core.ls = 100
#                 core.rd = 1
#                 core.rs = 100
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()



#             if boolean == 0:
#                 if counter < counter2:
#                     if abs(value2-340)> 100:
#                         #diagnol right
#                         core.ld = 1
#                         core.ls = 250
#                         core.rd = 1
#                         core.rs = 80
#                         # print("ok")
#                         pub.publish(core)
#                         rate.sleep()
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()

#                 else:
#                     if abs(value-340)>100:
#                         #left diagnol
#                         core.ld = 1
#                         core.ls = 80
#                         core.rd = 1
#                         core.rs = 250

#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")


#         # else:
#         #     #publish command to not start recovery node 
#         #     print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break












# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=340

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution





#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)


#         counter =1
#         counter2=1
#         counter3=1
#         value = 340
#         value2 = 340
       

#         for j in range(639,0,-1):
#             cal = 0
#             for i in range(479,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:
#                     cal = cal + 1
#                     obstacle[i][j] = (0,255,0)

#                 else:
#                     obstacle[i][j] = (0,0,255)
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)
#                 if j<639 and j>340:
#                     counter = counter + 1
#                     value = value +1
#                 if j<340 and j>40:
#                     counter2 = counter2 + 1
#                     value2 = value2 +1 
#                 if j<380 and j>260:
#                     counter3 = counter3+1                  
#             else :
#                 obstacle[0][j]=(0,255,255)

#         # for j in range(0,639):
#         #     cal = 0
#         #     for i in range(0,479):
#         #         if obstacle[i][j][1] == 255:
#         #             cal = cal+1
#         #     if cal > 350:
#         #         obstacle[0][j]=(255,0,0)

#         #     else :
#         #         obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         # counter =1
#         # counter2=1
#         # counter3=1
#         # value = 340
#         # value2 = 340

#         # for i in range(340,639):
#         #     if obstacle[0][i][0]==255 :
#         #         counter = counter +1
#         #         value = value + i #right

#         # for j in range (340,40,-1):
#         #     if obstacle[0][j][0]==255: 
#         #         counter2 = counter2 + 1
#         #         value2 = value2+j   #left
#         # for k in range (260,380):
#         #     if obstacle[0][k][0]==255:
#         #         counter3 = counter3 +1

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight

#         boolean = 0
#         boolean2 = 0

#         if counter3>165:
#             boolean2=1
#             core.ld=1
#             core.ls=200
#             core.rd=1
#             core.ls=200
#             pub.publish(core)
#             rate.sleep()


#         if boolean2 ==0:
#             if counter + counter2 < 10:
#                 #publish command to start recovery node and command to stop
#                 core.ld = 0
#                 core.ls = 0
#                 core.rd = 0
#                 core.rs = 0
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()
#                 print("not ok")

#             elif counter + counter2 > 550:
#                 core.ld = 1
#                 core.ls = 250
#                 core.rd = 1
#                 core.rs = 250
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()



#             if boolean == 0:
#                 if counter < counter2:
#                     if abs(value2-340)> 100:
#                         #diagnol right
#                         core.ld = 1
#                         core.ls = 80
#                         core.rd = 1
#                         core.rs = 250
#                         # print("ok")
#                         pub.publish(core)
#                         rate.sleep()
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()

#                 else:
#                     if abs(value-340)>100:
#                         #left diagnol
#                         core.ld = 1
#                         core.ls = 250
#                         core.rd = 1
#                         core.rs = 80

#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")


#         # else:
#         #     #publish command to not start recovery node 
#         #     print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break
















# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=340

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         cal = 0
#         counter =1
#         counter2=1
#         counter3=1
#         value = 340
#         value2 = 340
        
#         for j in range(639,0,-1):
#             for i in range(479,0,-1):    
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:

#                     obstacle[i][j] = (0,255,0)
#                     cal = cal+1
#                 else:
#                     obstacle[i][j] = (0,0,255)
#             if cal > 550:
#                 obstacle[0][j]=(255,0,0)
#                 if j>340:
#                     counter = counter +1 
#                     value = value + j 
#                 elif j<340 and j >40:
#                     counter2 = counter2+j
#                     value2 = value2+j
#                 elif j>260 and j<380:
#                     counter3 = counter3 + j

#             else :
#                 obstacle[0][j]=(0,255,255)


#         # for j in range(0,639):
#         #     cal = 0
#         #     for i in range(0,479):
#         #         if obstacle[i][j][1] == 255:
#         #             cal = cal+1

#                 # safe_path=safe_path+j




#         # for i in range(340,639):
#         #     if obstacle[0][i][0]==255 :
#         #         counter = counter +1
#         #         value = value + i #right

#         # for j in range (340,40,-1):
#         #     if obstacle[0][j][0]==255: 
#         #         counter2 = counter2 + 1
#         #         value2 = value2+j   #left
#         # for k in range (260,380):
#         #     if obstacle[0][k][0]==255:
#         #         counter3 = counter3 +1

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight

#         boolean = 0
#         boolean2 = 0

#         if counter3>165:
#             boolean2=1
#             core.ld=1
#             core.ls=200
#             core.rd=1
#             core.rs=200
#             pub.publish(core)
#             rate.sleep()


#         if boolean2 ==0:
#             if counter + counter2 < 10:
#                 #publish command to start recovery node and command to stop
#                 core.ld = 0
#                 core.ls = 0
#                 core.rd = 0
#                 core.rs = 0
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()
#                 print("not ok")

#             elif counter + counter2 > 550:
#                 core.ld = 1
#                 core.ls = 250
#                 core.rd = 1
#                 core.rs = 250
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()



#             if boolean == 0:
#                 if counter < counter2:
#                     if abs(value2-340)> 100:
#                         #diagnol right
#                         core.ld = 1
#                         core.ls = 80
#                         core.rd = 1
#                         core.rs = 250
#                         # print("ok")
#                         pub.publish(core)
#                         rate.sleep()
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()

#                 else:
#                     if abs(value-340)>100:
#                         #left diagnol
#                         core.ld = 1
#                         core.ls = 250
#                         core.rd = 1
#                         core.rs = 80

#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")


#         # else:
#         #     #publish command to not start recovery node 
#         #     print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break












# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=340

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         cal = 0
#         counter =1
#         counter2=1
#         counter3=1
#         value = 340
#         value2 = 340
        
#         for j in range(639,0,-1):
#             for i in range(479,0,-1):    
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:

#                     obstacle[i][j] = (0,255,0)
#                     cal = cal+1
#                 else:
#                     obstacle[i][j] = (0,0,255)
#             if cal > 550:
#                 obstacle[0][j]=(255,0,0)
#                 if j>340:
#                     counter = counter +1 
#                     value = value + j 
#                 elif j<340 and j >40:
#                     counter2 = counter2+j
#                     value2 = value2+j
#                 elif j>260 and j<380:
#                     counter3 = counter3 + j

#             else :
#                 obstacle[0][j]=(0,255,255)


#         # for j in range(0,639):
#         #     cal = 0
#         #     for i in range(0,479):
#         #         if obstacle[i][j][1] == 255:
#         #             cal = cal+1

#                 # safe_path=safe_path+j




#         # for i in range(340,639):
#         #     if obstacle[0][i][0]==255 :
#         #         counter = counter +1
#         #         value = value + i #right

#         # for j in range (340,40,-1):
#         #     if obstacle[0][j][0]==255: 
#         #         counter2 = counter2 + 1
#         #         value2 = value2+j   #left
#         # for k in range (260,380):
#         #     if obstacle[0][k][0]==255:
#         #         counter3 = counter3 +1

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight

#         boolean = 0
#         boolean2 = 0

#         if counter3>165:
#             boolean2=1
#             core.ld=1
#             core.ls=200
#             core.rd=1
#             core.rs=200
#             pub.publish(core)
#             rate.sleep()


#         if boolean2 ==0:
#             if counter + counter2 < 10:
#                 #publish command to start recovery node and command to stop
#                 core.ld = 0
#                 core.ls = 0
#                 core.rd = 0
#                 core.rs = 0
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()
#                 print("not ok")

#             elif counter + counter2 > 550:
#                 core.ld = 1
#                 core.ls = 250
#                 core.rd = 1
#                 core.rs = 250
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()



#             if boolean == 0:
#                 if counter < counter2:
#                     if abs(value2-340)> 100:
#                         #diagnol right
#                         core.ld = 1
#                         core.ls = 80
#                         core.rd = 1
#                         core.rs = 250
#                         # print("ok")
#                         pub.publish(core)
#                         rate.sleep()
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()

#                 else:
#                     if abs(value-340)>100:
#                         #left diagnol
#                         core.ld = 1
#                         core.ls = 250
#                         core.rd = 1
#                         core.rs = 80

#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")


#         # else:
#         #     #publish command to not start recovery node 
#         #     print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break











# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=340

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:

#                     obstacle[i][j] = (0,255,0)
#                 else:
#                     obstacle[i][j] = (0,0,255)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         counter =1
#         counter2=1
#         counter3=1
#         value = 340
#         value2 = 340

#         for i in range(340,639):
#             if obstacle[0][i][0]==255 :
#                 counter = counter +1
#                 value = value + i #right

#         for j in range (340,40,-1):
#             if obstacle[0][j][0]==255: 
#                 counter2 = counter2 + 1
#                 value2 = value2+j   #left
#         for k in range (260,380):
#             if obstacle[0][k][0]==255:
#                 counter3 = counter3 +1

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight

#         boolean = 0
#         boolean2 = 0

#         if counter3>165:
#             boolean2=1
#             core.ld=1
#             core.ls=200
#             core.rd=1
#             core.ls=200
#             pub.publish(core)
#             rate.sleep()


#         if boolean2 ==0:
#             if counter + counter2 < 10:
#                 #publish command to start recovery node and command to stop
#                 core.ld = 0
#                 core.ls = 0
#                 core.rd = 0
#                 core.rs = 0
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()
#                 print("not ok")

#             elif counter + counter2 > 550:
#                 core.ld = 1
#                 core.ls = 250
#                 core.rd = 1
#                 core.rs = 250
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()



#             if boolean == 0:
#                 if counter < counter2:
#                     if abs(value2-340)> 100:
#                         #diagnol right
#                         core.ld = 1
#                         core.ls = 80
#                         core.rd = 1
#                         core.rs = 250
#                         # print("ok")
#                         pub.publish(core)
#                         rate.sleep()
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()

#                 else:
#                     if abs(value-340)>100:
#                         #left diagnol
#                         core.ld = 1
#                         core.ls = 250
#                         core.rd = 1
#                         core.rs = 80

#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")


#         # else:
#         #     #publish command to not start recovery node 
#         #     print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break







# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=340

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:

#                     obstacle[i][j] = (0,255,0)
#                 else:
#                     obstacle[i][j] = (0,0,255)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         counter =1
#         counter2=1
#         counter3=1
#         value = 340
#         value2 = 340

#         for i in range(340,639):
#             if obstacle[0][i][0]==255 :
#                 counter = counter +1
#                 value = value + i #right

#         for j in range (340,40,-1):
#             if obstacle[0][j][0]==255: 
#                 counter2 = counter2 + 1
#                 value2 = value2+j   #left
#         for k in range (260,380):
#             if obstacle[0][k][0]==255:
#                 counter3 = counter3 +1

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight

#         boolean = 0
#         boolean2 = 0

#         if counter3>165:
#             boolean2=1
#             core.ld=1
#             core.ls=200
#             core.rd=1
#             core.ls=200
#             pub.publish(core)
#             rate.sleep()


#         if boolean2 ==0:
#             if counter + counter2 < 10:
#                 #publish command to start recovery node and command to stop
#                 core.ld = 0
#                 core.ls = 0
#                 core.rd = 0
#                 core.rs = 0
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()
#                 print("not ok")

#             elif counter + counter2 > 550:
#                 core.ld = 1
#                 core.ls = 250
#                 core.rd = 1
#                 core.rs = 250
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()



#             if boolean == 0:
#                 if counter < counter2:
#                     if abs(value2-340)> 100:
#                         #diagnol right
#                         core.ld = 1
#                         core.ls = 120     #make it 80 to make the diagnol turn faster 
#                         core.rd = 1
#                         core.rs = 250
#                         # print("ok")
#                         pub.publish(core)
#                         rate.sleep()
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()

#                 else:
#                     if abs(value-340)>100:
#                         #left diagnol
#                         core.ld = 1
#                         core.ls = 250
#                         core.rd = 1
#                         core.rs = 120

#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")


#         # else:
#         #     #publish command to not start recovery node 
#         #     print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break


























# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=320

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:

#                     obstacle[i][j] = (0,255,0)
#                 else:
#                     obstacle[i][j] = (0,0,255)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         counter =1
#         counter2=1
#         counter3=1
#         value = 320
#         value2 = 320

#         for i in range(320,639):
#             if obstacle[0][i][0]==255 :
#                 counter = counter +1
#                 value = value + i #right

#         for j in range (320,0,-1):
#             if obstacle[0][j][0]==255: 
#                 counter2 = counter2 + 1
#                 value2 = value2+j   #left
#         for k in range (260,380):
#             if obstacle[0][k][0]==255:
#                 counter3 = counter3 +1

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight

#         boolean = 0
#         boolean2 = 0

#         if counter3>165:
#             boolean2=1
#             core.ld=1
#             core.ls=200
#             core.rd=1
#             core.ls=200
#             pub.publish(core)
#             rate.sleep()


#         if boolean2 ==0:
#             if counter + counter2 < 10:
#                 #publish command to start recovery node and command to stop
#                 core.ld = 0
#                 core.ls = 0
#                 core.rd = 0
#                 core.rs = 0
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()
#                 print("not ok")

#             elif counter + counter2 > 550:
#                 core.ld = 1
#                 core.ls = 250
#                 core.rd = 1
#                 core.rs = 250
#                 boolean = 1
#                 pub.publish(core)
#                 rate.sleep()



#             if boolean == 0:
#                 if counter < counter2:
#                     if abs(value2-320)> 100:
#                         #diagnol right
#                         core.ld = 1
#                         core.ls = 250
#                         core.rd = 1
#                         core.rs = 120
#                         # print("ok")
#                         pub.publish(core)
#                         rate.sleep()
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()

#                 else:
#                     if abs(value-320)>100:
#                         #left diagnol
#                         core.ld = 1
#                         core.ls = 120
#                         core.rd = 1
#                         core.rs = 250

#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")
#                     else:
#                         #straight
#                         core.ld = 1
#                         core.ls = 150
#                         core.rd = 1
#                         core.rs = 150
#                         pub.publish(core)
#                         rate.sleep()
#                         # print("ok")


#         # else:
#         #     #publish command to not start recovery node 
#         #     print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break











# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=320

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:

#                     obstacle[i][j] = (0,255,0)
#                 else:
#                     obstacle[i][j] = (0,0,255)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         counter =1
#         counter2=1
#         value = 320
#         value2 = 320
#         for i in range(320,639):
#             if obstacle[0][i][0]==255 :
#                 counter = counter +1
#                 value = value + i #right

#         for j in range (320,0,-1):
#             if obstacle[0][j][0]==255: 
#                 counter2 = counter2 + 1
#                 value2 = value2+j   #left

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight

#         boolean = 0




#         if counter + counter2 < 10:
#             #publish command to start recovery node and command to stop
#             core.ld = 0
#             core.ls = 0
#             core.rd = 0
#             core.rs = 0
#             boolean = 1
#             pub.publish(core)
#             rate.sleep()
#             print("not ok")

#         elif counter + counter2 > 550:
#             core.ld = 1
#             core.ls = 250
#             core.rd = 1
#             core.rs = 250
#             boolean = 1
#             pub.publish(core)
#             rate.sleep()



#         if boolean == 0:
#             if counter < counter2:
#                 if abs(value2-320)> 100:
#                     #diagnol right
#                     core.ld = 1
#                     core.ls = 250
#                     core.rd = 1
#                     core.rs = 120
#                     # print("ok")
#                     pub.publish(core)
#                     rate.sleep()
#                 else:
#                     #straight
#                     core.ld = 1
#                     core.ls = 150
#                     core.rd = 1
#                     core.rs = 150
#                     pub.publish(core)
#                     rate.sleep()

#             else:
#                 if abs(value-320)>100:
#                     #left diagnol
#                     core.ld = 1
#                     core.ls = 120
#                     core.rd = 1
#                     core.rs = 250

#                     pub.publish(core)
#                     rate.sleep()
#                     # print("ok")
#                 else:
#                     #straight
#                     core.ld = 1
#                     core.ls = 150
#                     core.rd = 1
#                     core.rs = 150
#                     pub.publish(core)
#                     rate.sleep()
#                     # print("ok")


#         # else:
#         #     #publish command to not start recovery node 
#         #     print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break



















# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=320

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:
#                     obstacle[i][j] = (0,255,0)
#                 else:
#                     obstacle[i][j] = (0,0,255)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         counter =1
#         counter2=1
#         value = 320
#         value2 = 320
#         for i in range(320,639):
#             if obstacle[0][i][0]==255 :
#                 counter = counter +1
#                 value = value + i #right

#         for j in range (320,0,-1):
#             if obstacle[0][j][0]==255: 
#                 counter2 = counter2 + 1
#                 value2 = value2+j   #left

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight

#         boolean = 0




#         if counter + counter2 < 10:
#             #publish command to start recovery node and command to stop
#             core.ld = 0
#             core.ls = 0
#             core.rd = 0
#             core.rs = 0
#             boolean = 1
#             pub.publish(core)
#             rate.sleep()
#             print("not ok")

#         elif counter + counter2 > 550:
#             core.ld = 1
#             core.ls = 250
#             core.rd = 1
#             core.rs = 250
#             boolean = 1
#             pub.publish(core)
#             rate.sleep()



#         if boolean == 0:
#             if counter < counter2:
#                 if abs(value2-320)> 100:
#                     #diagnol right
#                     core.ld = 1
#                     core.ls = 120
#                     core.rd = 1
#                     core.rs = 250
#                     # print("ok")
#                     pub.publish(core)
#                     rate.sleep()
#                 else:
#                     #straight
#                     core.ld = 1
#                     core.ls = 150
#                     core.rd = 1
#                     core.rs = 150
#                     pub.publish(core)
#                     rate.sleep()

#             else:
#                 if abs(value-320)>100:
#                     #left diagnol
#                     core.ld = 1
#                     core.ls = 250
#                     core.rd = 1
#                     core.rs = 120

#                     pub.publish(core)
#                     rate.sleep()
#                     # print("ok")
#                 else:
#                     #straight
#                     core.ld = 1
#                     core.ls = 150
#                     core.rd = 1
#                     core.rs = 150
#                     pub.publish(core)
#                     rate.sleep()
#                     # print("ok")


#         # else:
#         #     #publish command to not start recovery node 
#         #     print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break





















# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=320

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:
#                     obstacle[i][j] = (0,255,0)
#                 else:
#                     obstacle[i][j] = (0,0,255)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         counter =1
#         counter2=1
#         value = 320
#         value2 = 320
#         for i in range(320,639):
#             if obstacle[0][i][0]==255 :
#                 counter = counter +1
#                 value = value + i #right

#         for j in range (320,0,-1):
#             if obstacle[0][j][0]==255: 
#                 counter2 = counter2 + 1
#                 value2 = value2+j   #left

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight



#         if counter < counter2:
#             if abs(value2-320)> 100:
#                 #diagnol right
#                 core.ld = 1
#                 core.ls = 120
#                 core.rd = 1
#                 core.rs = 250
#                 # print("ok")
#                 pub.publish(core)
#                 rate.sleep()
#             else:
#                 #straight
#                 core.ld = 1
#                 core.ls = 150
#                 core.rd = 1
#                 core.rs = 150
#                 pub.publish(core)
#                 rate.sleep()

#         else:
#             if abs(value-320)>100:
#                 #left diagnol
#                 core.ld = 1
#                 core.ls = 250
#                 core.rd = 1
#                 core.rs = 120

#                 pub.publish(core)
#                 rate.sleep()
#                 # print("ok")
#             else:
#                 #straight
#                 core.ld = 1
#                 core.ls = 150
#                 core.rd = 1
#                 core.rs = 150
#                 pub.publish(core)
#                 rate.sleep()
#                 # print("ok")

#         if counter + counter2 < 10:
#             #publish command to start recovery node and command to stop
#             core.ld = 0
#             core.ls = 0
#             core.rd = 0
#             core.rs = 0
#             pub.publish(core)
#             rate.sleep()
#             print("not ok")

#         elif counter + counter2 > 550:
#             core.ld = 1
#             core.ls = 250
#             core.rd = 1
#             core.rs = 250
#             pub.publish(core)
#             rate.sleep()

#         else:
#             #publish command to not start recovery node 
#             print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break






















# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=320

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     rospy.init_node('obstacle_avoidance',anonymous=True)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:
#                     obstacle[i][j] = (0,255,0)
#                 else:
#                     obstacle[i][j] = (0,0,255)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         counter =0
#         counter2=0
#         value = 320
#         value2 = 320
#         for i in range(320,639):
#             if obstacle[0][i][1]==255 and obstacle[0][i][2]==255:
#                 counter = counter +1
#                 value = value + i #right

#         for j in range (320,0,-1):
#             if obstacle[0][j][1]==255 and obstacle[0][j][2]==255:
#                 counter2 = counter2 + 1
#                 value2 = value2+j   #left

#         value = value//counter
#         value2 = value2// counter2

# # if counter + counter2 > < 550 or 50 then make value of threshhold 1 otherwise zero , and the commands below put ubder if of threshold == 0 executes only if it/threshold is 0 otherwise move straight



#         if value < value2:
#             if abs(value-320)> 100:
#                 #diagnol right
#                 core.ld = 1
#                 core.ls = 250
#                 core.rd = 1
#                 core.rs = 120
#                 # print("ok")
#                 pub.publish(core)
#                 rate.sleep()

#         else:
#             if abs(value2-320)>100:
#                 #left diagnol
#                 core.ld = 1
#                 core.ls = 120
#                 core.rd = 1
#                 core.rs = 250

#                 pub.publish(core)
#                 rate.sleep()
#                 # print("ok")
#             else:
#                 #straight
#                 core.ld = 1
#                 core.ls = 150
#                 core.rd = 1
#                 core.rs = 150
#                 pub.publish(core)
#                 rate.sleep()
#                 # print("ok")

#         if counter + counter2 < 10:
#             #publish command to start recovery node and command to stop
#             core.ld = 0
#             core.ls = 0
#             core.rd = 0
#             core.rs = 0
#             pub.publish(core)
#             rate.sleep()
#             print("not ok")

#         elif counter + counter2 > 550:
#             core.ld = 0
#             core.ls = 0
#             core.rd = 0
#             core.rs = 0
#             pub.publish(core)
#             rate.sleep()

#         else:
#             #publish command to not start recovery node 
#             print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break




















# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# safe_path=320

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     core = Drive()
#     rate = rospy.Rate(10)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:
#                     obstacle[i][j] = (0,255,0)
#                 else:
#                     obstacle[i][j] = (0,0,255)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 350:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)
#                 # safe_path=safe_path+j


#         counter =0
#         counter2=0
#         value = 320
#         value2 = 320
#         for i in range(320,639):
#             if obstacle[0][i][1]==255 and obstacle[0][i][2]==255:
#                 counter = counter +1
#                 value = value + i #right

#         for j in range (320,0,-1):
#             if obstacle[0][j][1]==255 and obstacle[0][j][2]==255:
#                 counter2 = counter2 + 1
#                 value2 = value2+j   #left

#         value = value//counter
#         value2 = value2// counter2
#         if value < value2:
#             if abs(value-320)> 100:
#                 #diagnol right
#                 core.ld = 1
#                 core.ls = 250
#                 core.rd = 1
#                 core.rs = 120
#                 # print("ok")
#                 pub.publish(core)
#                 rate.sleep()

#         else:
#             if abs(value2-320)>100:
#                 #left diagnol
#                 core.ld = 1
#                 core.ls = 120
#                 core.rd = 1
#                 core.rs = 250

#                 pub.publish(core)
#                 rate.sleep()
#                 # print("ok")
#             else:
#                 #straight
#                 core.ld = 1
#                 core.ls = 150
#                 core.rd = 1
#                 core.rs = 150
#                 pub.publish(core)
#                 rate.sleep()
#                 # print("ok")

#         if counter + counter2 < 10:
#             #publish command to start recovery node and command to stop
#             core.ld = 0
#             core.ls = 0
#             core.rd = 0
#             core.rs = 0
#             pub.publish(core)
#             rate.sleep()
#             print("not ok")
#         else:
#             #publish command to not start recovery node 
#             print("ok")




#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break

#give same lines of possible traversable at sides also like it is at top where blue indicates safe path relative to rover's centre, so if whole top half is red then we can tell how much free space is there in front of rover to manouvre itys way out














# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:
#                     obstacle[i][j] = (0,0,255)
#                 else:
#                     obstacle[i][j] = (0,255,0)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 50:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)


#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break







#single script to make the rover move which takes callbacks from all other nodes and take decisions on making rover move by prioritizing the nodes and their feedbacks.  






# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:
#                     obstacle[i][j] = (0,0,255)
#                 else:
#                     obstacle[i][j] = (0,255,0)


#         for j in range(0,639):
#             cal = 0
#             for i in range(0,479):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 50:
#                 obstacle[0][j]=(255,0,0)

#             else :
#                 obstacle[0][j]=(0,255,255)


#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break







# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(479,0,-1):
#             for j in range(639,0,-1):
#                 if depth_frame[i,j] - depth_frame[i-1,j]> 5:
#                     obstacle[i][j] = (0,0,255)
#                 else:
#                     obstacle[i][j] = (0,255,0)


#         # for j in range(0,639):
#         #     cal = 0
#         #     for i in range(0,479):
#         #         if obstacle[i][j][1] == 255:
#         #             cal = cal+1
#         #     if cal > 150:
#         #         obstacle[0][j]=(255,0,0)

#         #     else :
#         #         obstacle[0][j]=(0,255,255)


#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break






# #! /usr/bin/env python
# import rospy
# from atom_drive.msg import Drive

# import cv2
# #import pyrealsense2
# import pyrealsense2 as rs
# import numpy as np

# class DepthCamera:
#     def __init__(self):
#         # Configure depth and color streams
#         self.pipeline = rs.pipeline()
#         config = rs.config()

#         # Get device product line for setting a supporting resolution
#         pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
#         pipeline_profile = config.resolve(pipeline_wrapper)
#         device = pipeline_profile.get_device()
#         device_product_line = str(device.get_info(rs.camera_info.product_line))

#         config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#         config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)



#         # Start streaming
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

# point = (400,300)      
# def show_distance(event,x,y,args,params):
#     global point
#     print(x,y)


# dc = DepthCamera()

# cv2.namedWindow("Color frame")
# cv2.setMouseCallback("Color frame",show_distance)



# if __name__ == '__main__':
#     list = []

#     pub = rospy.Publisher('calibrate/auto', Drive, queue_size=20)
#     # subscriber()
#     # subscriber2()
# #    straight(pub,core,rate,yaw,t)
#     # publisher(pub)
#     while True:
#         ret,depth_frame,color_frame = dc.get_frame()
#         cv2.namedWindow("obstacle",cv2.WINDOW_NORMAL)
        
#         obstacle = color_frame
#         # cv2.circle(color_frame,point,4,(0,0,255))
#         distance = depth_frame[point[1],point[0]]
        
#         print(distance)
        
#         cv2.putText(color_frame,"{}mm".format(distance),(point[0],point[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        
#         cv2.imshow("depth frame",depth_frame)
#         cv2.imshow("Color frame",color_frame)
#         # obstacle[20][50]  = (0,0,255)
#         for i in range(0,479):
#             for j in range(0,639):
#                 if depth_frame[i,j] - depth_frame[i-1,j-1]> 5:
#                     obstacle[i][j] = (0,0,255)
#                 else:
#                     obstacle[i][j] = (0,255,0)


#         for i in range(0,479):
#             cal = 0
#             for j in range(0,639):
#                 if obstacle[i][j][1] == 255:
#                     cal = cal+1
#             if cal > 150:
#                 var = "yes"
#                 list.append(var)
#             else :
#                 var = "no"
#                 list.append(var)

#         cv2.imshow("obstacle",obstacle)
#         # cv2.imshow("good",list)
#         print(list)
#         key=cv2.waitKey(1)
#         if key==27:
#             break

##make top line pixels blue for paths which are traversable