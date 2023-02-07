
import cv2
from time import sleep
from Library import config as cfg
from Library.imageProcessor import processFrame


import os, shutil


cap=cv2.VideoCapture(0)

if not os.path.exists("./Frames/"):
	os.mkdir("./Frames")
	print("Created new directory for logging frames")
else:
	shutil.rmtree('./Frames')
	os.mkdir('./Frames')
	print ('Re-created frames directory')

frames = 0

try:

	while(1):
		

		detectedAngle = processFrame()

		if detectedAngle != None:
			if (detectedAngle < 0):
				print ('Detected right arrow')

			elif (detectedAngle > 0):
				print ('Detected left arrow')

		else:
			print ('No arrow detected')


		frames += 1

except KeyboardInterrupt:
	cap.release()	
