#!/usr/bin/env python

import rospy
import csv

from std_msgs.msg import Float32
import datetime
from doorBot.msg import my_msgs
class plotclass:
	def __init__(self):
		
		rospy.init_node('traj_node', anonymous=True)
		self.xarray=[]
		self.darray=[]
		
		self.nowTime=datetime.datetime.now() 
		self.out = open('/home/saeid/catkin_ws/src/doorBot/Traj/'+str(self.nowTime)+'.csv', 'a')
		self.out.write('%s,' % 'x')
		self.out.write('%s,' % 'y(d)')
		self.out.write('\n')
		rospy.Subscriber("traj_topic", my_msgs, self.callback)
		#while not rospy.is_shutdown():
		#	a=1                     
	
	def callback(self,data):
	
		
		self.xarray.append(-1.0*data.x)
		self.darray.append(-1.0*data.y)
		
		tempx=-1.0*float(data.x)
		tempd=-1.0*float(data.y)
		self.out.write('%f,' % tempx)
		self.out.write('%f,' % tempd)
		self.out.write('\n')

	def shutdown(self):
		# stop turtlebot
		rospy.loginfo("Stop Saving trajectory")
		self.out.close()
		rospy.sleep(1)

			

def main():

	x=plotclass()
	rospy.spin()

if __name__=="__main__":
	main()