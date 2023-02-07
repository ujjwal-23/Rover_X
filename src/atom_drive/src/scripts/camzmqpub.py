# run this program on each RPi to send a labelled image stream
import cv2
import socket
import time
from imutils.video import VideoStream
import imagezmq
  
sender = imagezmq.ImageSender(connect_to='tcp://devanshu-inspiron-5502:5555')
#cap=cv2.VideoCapture(0)
rpi_name = socket.gethostname() # send RPi hostname with each image
picam = VideoStream(src=0,).start()
time.sleep(2.0)  # allow camera sensor to warm up
print("sending image")
while True:  # send images as stream until Ctrl-C
    image = picam.read()
    sender.send_image(rpi_name, image)
    print("sending image")
