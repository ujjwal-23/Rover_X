import cv2


cap = cv2.VideoCapture('rtsp://admin:RoverX123@192.168.1.64/8000')


while True:

    
    ret, frame = cap.read()
    
    cv2.imshow("Capturing",frame)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
