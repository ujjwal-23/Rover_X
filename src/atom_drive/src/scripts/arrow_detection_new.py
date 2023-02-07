import time
import cv2
import numpy as np

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

cap = cv2.VideoCapture(0)
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
kernel = np.ones((5,5),np.uint8)

def getContours(inImg, outImg):
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
                cv2.putText(outImg, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                            (0, 255, 0), 2)
                cv2.putText(outImg, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)
                cv2.drawContours(outImg, [approx], -1, (0, 255, 0), 2)
                _, _, angle = cv2.fitEllipse(approx)
                if (angle > 80 and angle < 100):
                    xval = list(approx[:, 0, 0])
                    arrow_center = (max(xval) + min(xval)) / 2
                    if np.median(xval) < arrow_center:
                       print("left")
                    else:
                        print("right")


try:
    while True:
        success, img = cap.read()
        imgOut = img.copy()
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray,(3,3),0)

        imgCanny = cv2.Canny(imgBlur,30,100)
        imgDilated = cv2.dilate(imgCanny, kernel, iterations = 2)
        imgEroded = cv2.erode(imgDilated, kernel, iterations = 1)

        getContours(imgEroded, imgOut)
        allImages = stackImages(0.5,([img, imgGray, imgOut],
                                       [imgCanny, imgDilated, imgEroded]))

        cv2.imshow("Image processing", allImages)
        if cv2.waitKey(1) and 0xFF == ord('q'):
           break
except Exception as ex:
    print(ex)
finally:
    cap.release()
