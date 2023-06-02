#! /usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32
from atom_drive.msg import Drive

val = 1
x=1
def subscriber():
    rospy.init_node('recovery_waala',anonymous=True)
    rospy.Subscriber('/stuck',Float32,callback)

def callback(data):
    global x 
    x = data.data

def publisher(pub):
    if x == 1:
        core=Drive()
        rate = rospy.Rate(10)

        for i in range(0,100):
            if i%8==0:
                val = -1*val
            if val==1:

                core.ld = 2
                core.ls = 120
                core.rd = 1
                core.rs = 120

                pub.publish(core)
                rate.sleep()   
            else:
                core.ld = 1
                core.ls = 120   
                core.rd = 2
                core.rs = 120
                pub.publish(core)
                rate.sleep()        
  
        for i in range(0,100):
            core.ld = 2
            core.ls = 120
            core.rd = 2
            core.rs = 120

            pub.publish(core)
            rate.sleep()    
        for i in range(0,100):
            if i%8==0:
                val = -1*val
            if val==1:

                core.ld = 2
                core.ls = 120
                core.rd = 1
                core.rs = 120

                pub.publish(core)
                rate.sleep()   
            else:
                core.ld = 1
                core.ls = 120
                core.rd = 2
                core.rs = 120

                pub.publish(core)
                rate.sleep()  

    elif x==2:
        core = Drive()
        rate=rospy.Rate(10)
        while x ==2:

            core.ld = 2
            core.ls = 120
            core.rd = 2
            core.rs = 120

            pub.publish(core)
            rate.sleep()  


    # for i in range(0,100):
    #     core.ld = 2
    #     core.ls = 120
    #     core.rd = 1
    #     core.rs = 120

    #     pub.publish(core)
    #     rate.sleep()   


if __name__=="__main__":
    pub=rospy.Publisher('calibrate/auto',Drive,queue_size=20)
    # subscriber()
    publisher()







# #! /usr/bin/env python
# import rospy
# import numpy as np
# from std_msgs.msg import Float32
# from atom_drive.msg import Drive

# val = 1

# def subscriber():
#     rospy.init_node('recovery_waala',anonymous=True)
#     rospy.Subscriber('/stuck',Float32,callback)

# def callback(data):
#     global x 
#     x = data.data

# #store all depth frame values in a matrix so dont call it again and again

# def publisher(pub):
#     if x == 1:
#         core=Drive()
#         rate = rospy.Rate(10)

#         for i in range(0,100):
#             if i%8==0:
#                 val = -1*val
#             if val==1:

#                 core.ld = 2
#                 core.ls = 120
#                 core.rd = 1
#                 core.rs = 120

#                 pub.publish(core)
#                 rate.sleep()   
#             else:
#                 core.ld = 1
#                 core.ls = 120   
#                 core.rd = 2
#                 core.rs = 120
#                 pub.publish(core)
#                 rate.sleep()        
  
#         for i in range(0,100):
#             core.ld = 2
#             core.ls = 120
#             core.rd = 2
#             core.rs = 120

#             pub.publish(core)
#             rate.sleep()    
#         for i in range(0,100):
#             if i%8==0:
#                 val = -1*val
#             if val==1:

#                 core.ld = 2
#                 core.ls = 120
#                 core.rd = 1
#                 core.rs = 120

#                 pub.publish(core)
#                 rate.sleep()   
#             else:
#                 core.ld = 1
#                 core.ls = 120
#                 core.rd = 2
#                 core.rs = 120

#                 pub.publish(core)
#                 rate.sleep()  

#     elif x==2:
#         core = Drive()
#         rate=rospy.Rate(10)
#         while x ==2:

#             core.ld = 2
#             core.ls = 120
#             core.rd = 2
#             core.rs = 120

#             pub.publish(core)
#             rate.sleep()  


#     # for i in range(0,100):
#     #     core.ld = 2
#     #     core.ls = 120
#     #     core.rd = 1
#     #     core.rs = 120

#     #     pub.publish(core)
#     #     rate.sleep()   


# if __name__=="__main__":
#     pub=rospy.Publisher('calibrate/auto',Drive,queue_size=20)
#     subscriber()
#     publisher()













# #! /usr/bin/env python
# import rospy
# import numpy as np
# from std_msgs.msg import Float32
# from atom_drive.msg import Drive

# val = 1

# def subscriber():
#     rospy.init_node('recovery_waala',anonymous=True)
#     rospy.Subscriber('/stuck',Float32,callback)

# def callback(data):
#     global x 
#     x = data.data



# def publisher(pub):
#     if x == 1:
#         core=Drive()
#         rate = rospy.Rate(10)

#         for i in range(0,100):
#             if i%8==0:
#                 val = -1*val
#             if val==1:

#                 core.ld = 2
#                 core.ls = 120
#                 core.rd = 1
#                 core.rs = 120

#                 pub.publish(core)
#                 rate.sleep()   
#             else:
#                 core.ld = 1
#                 core.ls = 120            if counter < counter2:
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
#                 core.rd = 2
#                 core.rs = 120

#                 pub.publish(core)
#                 rate.sleep()    
#         for i in range(0,100):
#             core.ld = 2
#             core.ls = 120
#             core.rd = 2
#             core.rs = 120

#             pub.publish(core)
#             rate.sleep()    
#         for i in range(0,100):
#             if i%8==0:
#                 val = -1*val
#             if val==1:

#                 core.ld = 2
#                 core.ls = 120
#                 core.rd = 1
#                 core.rs = 120

#                 pub.publish(core)
#                 rate.sleep()   
#             else:
#                 core.ld = 1
#                 core.ls = 120
#                 core.rd = 2
#                 core.rs = 120

#                 pub.publish(core)
#                 rate.sleep()  

#     elif x==2:
#         core = Drive()
#         rate=rospy.Rate(10)
#         while x ==2:

#             core.ld = 2
#             core.ls = 120
#             core.rd = 2
#             core.rs = 120

#             pub.publish(core)
#             rate.sleep()  


#     # for i in range(0,100):
#     #     core.ld = 2
#     #     core.ls = 120
#     #     core.rd = 1
#     #     core.rs = 120

#     #     pub.publish(core)
#     #     rate.sleep()   


# if __name__=="__main__":
#     pub=rospy.Publisher('/move',Drive,queue_size=20)
#     subscriber()
#     publisher()