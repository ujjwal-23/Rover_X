import time
import cv2
import imutils
import numpy as np
import pyrealsense2 as rs

BOX_HEIGHT = 0
BOX_WIDTH = 0
ARROW_CENTER=0,0
POINT=[270,250]

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

      
def show_distance(event,x,y,args,params):
    global POINT
    print(x,y)


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



def getContours(inImg, outImg,finalImg):
    global ARROW_CENTER 
    contours, hierarchy = cv2.findContours(inImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            cv2.drawContours(outImg, cnt, -1, (255, 0, 255), 7)
            #find closed contours
            peri = cv2.arcLength(cnt, True)           
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #number of points
#            print(len(approx))
            if(len(approx) == 7):
                print("arrow")            
                x , y , w, h = cv2.boundingRect(approx)
                cv2.rectangle(outImg, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
                cv2.rectangle(color_frame, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
                cv2.putText(outImg, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                cv2.putText(outImg, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)
                cv2.drawContours(outImg, [approx], -1, (0, 255, 0), 2)
                _, _, angle = cv2.fitEllipse(approx)
                BOX_HEIGHT=y+h/2
                BOX_WIDTH=x+w/2
                POINT=[BOX_HEIGHT,BOX_WIDTH]
                
                
#                distance = depth_frame(POINT[1],POINT[0])
#                cv2.putText(color_frame,"{}mm".format(distance),(POINT[0],POINT[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
                
                
#                print(BOX_HEIGHT,BOX_WIDTH)
#                print(POINT)
                if (angle > 80 and angle < 100):
                    xval = list(approx[:, 0, 0])
                    ARROW_CENTER = (max(xval) + min(xval)) / 2
#                    point = arrow_centre
                    if np.median(xval) < ARROW_CENTER:
                        print("left")
                        cv2.putText(finalImg,"left",(290,270),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
                    else:
                        print("right")
                        cv2.putText(finalImg,"right",(290,270),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
    return ARROW_CENTER

dc = DepthCamera()

#cap = cv2.VideoCapture(0)
#frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
kernel = np.ones((5,5),np.uint8)

cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame",show_distance)

try:
    while True:
#        success, img = cap.read()
        
        ret,depth_frame,color_frame = dc.get_frame()
        
        
        imgOut = color_frame.copy()
        imgGray = cv2.cvtColor(color_frame,cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray,(3,3),0)

        imgCanny = cv2.Canny(imgBlur,30,100)
        imgDilated = cv2.dilate(imgCanny, kernel, iterations = 2)
        imgEroded = cv2.erode(imgDilated, kernel, iterations = 1)
        getContours(imgEroded, imgOut, color_frame)
#        print(POINT)
#        point = getContours(imgEroded, imgOut)
        allImages = stackImages(0.5,([color_frame, imgGray, imgOut],[imgCanny, imgDilated, imgEroded]))

        cv2.imshow("Image processing", allImages)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
#        point = [BOX_WIDTH,BOX_HEIGHT]
        print(BOX_WIDTH)
#        POINT = 270,250
#        print(point)
#        point = ARROW_CENTER
#        point = ARROW_CENTER
#        cv2.circle(color_frame,point,4,(0,0,255))
        distance = depth_frame[POINT[1],POINT[0]]
#        print("yes")
    
#        print(distance)
#        print(POINT)
    
        cv2.putText(color_frame,"{}mm".format(distance),(POINT[0],POINT[1]),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
        color_frame=imutils.resize(color_frame,width=550)
        cv2.imshow("depth frame",depth_frame)
        cv2.imshow("Color frame",color_frame)
        key=cv2.waitKey(1)
        if key==27:
            break        
        
        
except Exception as ex:
    print(ex)
#finally:
#    cap.release()


"""

import time
import cv2
import imutils
import numpy as np
import pyrealsense2 as rs

BOX_HEIGHT = 0
BOX_WIDTH = 0
ARROW_CENTER=0,0
POINT=[270,250]

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

      
def show_distance(event,x,y,args,params):
    global POINT
    print(x,y)


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



def getContours(inImg, outImg):
    global ARROW_CENTER 
    contours, hierarchy = cv2.findContours(inImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            cv2.drawContours(outImg, cnt, -1, (255, 0, 255), 7)
            #find closed contours
            peri = cv2.arcLength(cnt, True)           
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #number of points
#            print(len(approx))
            if(len(approx) == 7):
                print("arrow")            
                x , y , w, h = cv2.boundingRect(approx)
                cv2.rectangle(outImg, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
                cv2.rectangle(color_frame, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
                cv2.putText(outImg, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                cv2.putText(outImg, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)
                cv2.drawContours(outImg, [approx], -1, (0, 255, 0), 2)
                _, _, angle = cv2.fitEllipse(approx)
                BOX_HEIGHT=y+h/2
                BOX_WIDTH=x+w/2
                POINT=[BOX_HEIGHT,BOX_WIDTH]
                
                
#                distance = depth_frame(POINT[1],POINT[0])
#                cv2.putText(color_frame,"{}mm".format(distance),(POINT[0],POINT[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
                
                
#                print(BOX_HEIGHT,BOX_WIDTH)
#                print(POINT)
                if (angle > 80 and angle < 100):
                    xval = list(approx[:, 0, 0])
                    ARROW_CENTER = (max(xval) + min(xval)) / 2
#                    point = arrow_centre
                    if np.median(xval) < ARROW_CENTER:
                        print("left")
                    else:
                        print("right")
    return ARROW_CENTER

dc = DepthCamera()

#cap = cv2.VideoCapture(0)
#frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
kernel = np.ones((5,5),np.uint8)

cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame",show_distance)

try:
    while True:
#        success, img = cap.read()
        
        ret,depth_frame,color_frame = dc.get_frame()
        
        
        imgOut = color_frame.copy()
        imgGray = cv2.cvtColor(color_frame,cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray,(3,3),0)

        imgCanny = cv2.Canny(imgBlur,30,100)
        imgDilated = cv2.dilate(imgCanny, kernel, iterations = 2)
        imgEroded = cv2.erode(imgDilated, kernel, iterations = 1)
        getContours(imgEroded, imgOut)
#        print(POINT)
#        point = getContours(imgEroded, imgOut)
        allImages = stackImages(0.5,([color_frame, imgGray, imgOut],[imgCanny, imgDilated, imgEroded]))

        cv2.imshow("Image processing", allImages)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
#        point = [BOX_WIDTH,BOX_HEIGHT]
        print(BOX_WIDTH)
#        POINT = 270,250
#        print(point)
#        point = ARROW_CENTER
#        point = ARROW_CENTER
#        cv2.circle(color_frame,point,4,(0,0,255))
        distance = depth_frame[POINT[1],POINT[0]]
#        print("yes")
    
#        print(distance)
#        print(POINT)
    
        cv2.putText(color_frame,"{}mm".format(distance),(POINT[0],POINT[1]),cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),2)
        color_frame=imutils.resize(color_frame,width=550)
        cv2.imshow("depth frame",depth_frame)
        cv2.imshow("Color frame",color_frame)
        key=cv2.waitKey(1)
        if key==27:
            break        
        
        
except Exception as ex:
    print(ex)
#finally:
#    cap.release()

"""   
    
    
   



