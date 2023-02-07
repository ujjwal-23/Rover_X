#! /usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from atom_drive.msg import Core
from std_msgs.msg import Int32MultiArray
import time


class Joystick:
    def __init__(self) -> None:

        # rospy.init_node('joystick_node', anonymous=True)
        rospy.Subscriber('joy0', Joy, self.core_callback)

        self.axes = [0, 0, 0, 0, 0, 0]
        self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.LD = 0
        self.RD = 0
        self.LS = 0
        self.RS = 0

    def core_callback(self, data):
        self.axes = list(data.axes)
        self.buttons = list(data.buttons)

    def set_nav_values(self):

        '''sets values for array to send STM1 for navigaion '''

        # # Turn Left 
         #if  self.axes[0]>0 and self.axes[1]>0:
         #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
         #    self.LD = 1 
         #    self.RD = 1
         #    self.LS = int(high_speed/2)
         #    self.RS = int(high_speed)
        # # Turn Right
         #elif self.axes[0]<0 and self.axes[1]>0:
         #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
         #    self.LD = 1 
         #    self.RD = 1
         #    self.LS = int(high_speed)
         #    self.RS = int(high_speed/2)
        # # Turn Reverse Right
         #elif self.axes[0]>0 and self.axes[1]<0:
         #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
         #    self.LD = 2 
         #    self.RD = 2
         #    self.LS = int(high_speed/2)
         #    self.RS = int(high_speed)
        # # Turn Reverse Left
         #elif self.axes[0]<0 and self.axes[1]<0:
         #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
         #    self.LD=2
         #    self.RD=2
         #    self.LS=int(high_speed)
         #    self.RS=int(high_speed/2)
        # Forward
        if self.axes[1]>0: 
            self.LD=1
            self.RD=1
            self.LS=int(abs(self.axes[1]*250))
            self.RS=int(abs(self.axes[1]*250))
        # Backward
        elif self.axes[1]<0:
            self.LD=2
            self.RD=2
            self.LS=int(abs(self.axes[1]*250))
            self.RS=int(abs(self.axes[1]*250))
        # Left
        elif self.axes[0]>0: 
            self.LD=2
            self.RD=1
            self.LS=int(abs(self.axes[0]*250))
            self.RS=int(abs(self.axes[0]*250))
        # Right
        elif self.axes[0]<0: #right
            self.LD=1
            self.RD=2
            self.LS=int(abs(self.axes[0]*250))
            self.RS=int(abs(self.axes[0]*250))
        # Default zero
        if self.axes[0] == 0 and self.axes[1] == 0:
            self.LD = 0
            self.RD = 0
            self.LS = 0
            self.RS = 0

        
    
    def limit_value(self, value, low, high):
        if value < low:
            value = low
        if value > high:
            value = high
        return value





#! /usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from atom_drive.msg import Core
from std_msgs.msg import Int32MultiArray
import time


class Joystick:
    def __init__(self) -> None:

        # rospy.init_node('joystick_node', anonymous=True)
        rospy.Subscriber('joy0', Joy, self.core_callback)

        self.axes = [0, 0, 0, 0, 0, 0]
        self.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.LD = 0
        self.RD = 0
        self.LS = 0
        self.RS = 0

    def core_callback(self, data):
        self.axes = list(data.axes)
        self.buttons = list(data.buttons)
        
    def map(x,y):
    	centre_y=0.2
    	centre_x=0.2
    	y_val=float(abs((y-centre_y)*250))
    	x_val=float(abs((x-centre_x)*250))
    	return [x_val,y_val]

    def set_nav_values(self):

        '''sets values for array to send STM1 for navigaion '''

        # # Turn Left 
        #if  self.axes[0]>0 and self.axes[1]>0:
        #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
        #    self.LD = 1 
        #    self.RD = 1
        #    self.LS = int(high_speed/2)
        #    self.RS = int(high_speed)
        # # Turn Right
        #elif self.axes[0]<0 and self.axes[1]>0:
        #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
        #    self.LD = 1 
        #    self.RD = 1
        #    self.LS = int(high_speed)
        #    self.RS = int(high_speed/2)
        # # Turn Reverse Right
        #elif self.axes[0]>0 and self.axes[1]<0:
        #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
        #    self.LD = 2 
        #    self.RD = 2
        #    self.LS = int(high_speed/2)
        #    self.RS = int(high_speed)
        # # Turn Reverse Left
        #elif self.axes[0]<0 and self.axes[1]<0:
      
        #    high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
        #    self.LD=2
        #    self.RD=2
        #    self.LS=int(high_speed)
        #    self.RS=int(high_speed/2)
        if self.axes[1]>=0:
        	val_y=map(self.axes[0],self.axes[1])[1]
        	val_x=map(self.axes[0],self.axes[1])[0] 
        	self.LD=1
        	self.RD=1
        	if self.axes[0]<0:
        		self.LS=int(250*(1-val_X))
        		self.RS=250
        				     		
        	if self.axes[0]>0:
        		self.LS=250
        		self.RS=int(250*(1-val_X))
        if self.axes[1]==1:
        	high_speed=(int(abs(self.axes[0]*250))+int(abs(self.axes[1]*250)))/2
        	while self.axes[1]==1 :
        		rotation=int(abs(self.axes[0]*250))
        		
        		if self.axes[0]>=0:
        		   	self.LD=1
        			self.RD=1
        			self.LS=high_speed/rotation
        			self.RS=250

        		if self.axes[0]<0:
        		   	self.LD=1
        			self.RD=1
        			self.LS=250
        			self.RS=high_speed/rotation 
        # Forward
        elif self.axes[1]>0: 
            self.LD=1
            self.RD=1
            self.LS=int(abs(self.axes[1]*250))
            self.RS=int(abs(self.axes[1]*250))
        # Backward
        elif self.axes[1]<0:
            self.LD=2
            self.RD=2
            self.LS=int(abs(self.axes[1]*250))
            self.RS=int(abs(self.axes[1]*250))
        # Left
        elif self.axes[0]>0: 
            self.LD=2
            self.RD=1
            self.LS=int(abs(self.axes[0]*250))
            self.RS=int(abs(self.axes[0]*250))
        # Right
        elif self.axes[0]<0: #right
            self.LD=1
            self.RD=2
            self.LS=int(abs(self.axes[0]*250))
            self.RS=int(abs(self.axes[0]*250))
        # Default zero
        if self.axes[0] == 0 and self.axes[1] == 0:
            self.LD = 0
            self.RD = 0
            self.LS = 0
            self.RS = 0
 
        

        				             	
        	
        
    
    def limit_value(self, value, low, high):
        if value < low:
            value = low
        if value > high:
            value = high
        return value
        
        
# no integer waali bakchodi - use uint8 - , map to 0 and 255 , make functions on 1 or 0 to change between codes for joysticks , mark the dead zones of the different joysticks and map accordingly .  
#map the joystick between the dead zone and the max value from 0 to 250 and define the dead zone as centre max so map from centre max to max .dead zone - area before which the origin doesnt shift/change the value very quickly. also while doing calculations - consider the variables to be float and then round them off in the end to send them as uint8 as then between calculations 0.8 would get rounded off to 0/1.       
  






