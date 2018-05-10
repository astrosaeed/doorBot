#!/usr/bin/env python

import rospy
import csv
import matplotlib.pyplot as plt
from std_msgs.msg import Float32
import datetime
from doorBot.msg import my_msgs

class plotclass:
	def __init__(self):
		
		rospy.init_node('plot_node', anonymous=True)
		self.xarray=[]
		self.darray=[]
		self.nowTime=datetime.datetime.now()
		self.filename= '/home/saeid/catkin_ws/src/doorBot/Plots/'+str(self.nowTime)+'.png'
		rospy.Subscriber("traj_topic", my_msgs, self.callback)
		#while not rospy.is_shutdown():
			#self.plot()
		#	rospy.loginfo('I am plotting')
	def callback(self,data):
		
		self.xarray.append(-1.0*data.x)
		self.darray.append(-1.0*data.y)
		self.plot()
		
	
	def shutdown(self):
	   
		rospy.loginfo("Stop Segbot")
		rospy.sleep(1)
		#self.plot()


	def plot(self):
		plt.plot(0,0,'*')
		plt.plot(self.xarray,self.darray)
		plt.xlabel('X values')
		plt.ylabel('Y values')
		plt.grid(True)
		plt.axis((-5,+5,-7,2))
		plt.savefig(self.filename)

def main():

	x=plotclass()
	rospy.spin()

if __name__=="__main__":
	main()
