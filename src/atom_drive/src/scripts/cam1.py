import cv2
import imutils
cap2 = cv2.VideoCapture("rtsp://admin:RoverX123@192.168.1.64/1")
while(True):
    ret2,im2 = cap2.read()

    cv2.imshow("ip_cam",imutils.resize(im2,width=1080))
#    cv2.imshow("ip_cam",im2)
    cv2.waitKey(1)
