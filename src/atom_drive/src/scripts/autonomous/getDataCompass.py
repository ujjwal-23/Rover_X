#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import MagneticField
import math

# count = 0
# final = None

class subsClass:
	count = 0
	final = None
	def __init__(self, parent=None):
		rospy.init_node('getPhoneData', anonymous=True)
		rospy.Subscriber("phone1/android/magnetic_field", MagneticField, self.callback,queue_size=1)	
		rospy.spin()


	def callback(self,data):
		global count, final
		try:
			x = data.magnetic_field.x
			y = data.magnetic_field.y
			z = data.magnetic_field.z
			compass = round(math.atan2(y,x)*180/math.pi,1)
			compass = (compass-90)
			if(compass<0):
				compass += 360
			print ("x : "+ str(x))
			print ("y : "+ str(y))
			print ("z : "+ str(z))
			print ("\nCompass : "+ str(compass))
			#print ("\nCount : "+ str(self.count))
			final = str(compass)
			#print("\n")
			time.sleep(0.1)

		except Exception as e:
			final = '1000'
			print("[Compass Module] Error : "+ str(e))

		finally:
			if(self.count>999):
				fs=open("COMPASS.txt","w")
				fs.write(final+"\n")
				fs.close()
				self.count=0
			else:
				fs=open("COMPASS.txt","a")
				fs.write(final+"\n")
				fs.close()
				self.count+=1

if __name__ == '__main__':
	obj=subsClass()


