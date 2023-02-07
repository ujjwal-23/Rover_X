import cv2 
import imutils
import numpy as np
#cap1=cv2.VideoCapture(0)
#cap2=cv2.VideoCapture('rtsp://admin:RoverX123@192.168.1.64/1')
cap3=cv2.VideoCapture(5)

while True:
#    _1,img1=cap1.read()
#    _2,img2=cap2.read()
    _3,img3=cap3.read()

#    newimg=np.concatenate((img1,imutils.resize(img2,width=854)),1)
#    newimg1=np.concatenate((img3,imutils.resize(img3,width=854)),1)
    img3=imutils.resize(img3,width=400,height=500)
    cv2.imshow("cap",img3)
    #cv2.imshow("cap2",img3)
    cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()










"""
import cv2 
import imutils
import numpy as np
cap1=cv2.VideoCapture(0)
cap2=cv2.VideoCapture('rtsp://admin:RoverX123@192.168.1.64/1')
cap3=cv2.VideoCapture(2)

while True:
    _1,img1=cap1.read()
    _2,img2=cap2.read()
    _3,img3=cap3.read()

    newimg=np.concatenate((img1,imutils.resize(img2,width=854)),1)
    newimg1=np.concatenate((img3,newimg),1)

    cv2.imshow("cap",newimg1)
    #cv2.imshow("cap2",img3)
    cv2.waitKey(0)
"""
    






"""
import numpy as np
import cv2
import imutils

index = 0
arr = []
while True:
    cap = cv2.VideoCapture(index)

    if not cap.read()[0]:
        break
    else:
        arr.append(index)
    cap.release()
    index += 1

video_captures = [cv2.VideoCapture(idx) for idx in arr]
while True:
    # Capture frame-by-frame
    frames = []
    frames_preview = []

    for i in arr:
        # skip webcam capture
        if i == 1: continue
        ret, frame = video_captures[i].read()
        if ret:
            frames.append(frame)
            small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            frames_preview.append(small)

    for i, frame in enumerate(frames_preview):
        cv2.imshow('Cam {}'.format(i), frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
for video_capture in video_captures:
    video_capture.release()
cv2.destroyAllWindows()
"""
