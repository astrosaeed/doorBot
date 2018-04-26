#!/usr/bin/env python

import rospy
import csv
import matplotlib.pyplot as plt
from std_msgs.msg import Float32
import datetime

class plotclass:
	def __init__(self):
		
		rospy.init_node('plot_node', anonymous=True)
		self.xarray=[]
		self.darray=[]
		
		#self.nowTime=rospy.Time.now() 
		self.nowTime=datetime.datetime.now() 

		rospy.Subscriber("trajx_topic", Float32, self.xcallback)
		rospy.Subscriber("trajd_topic", Float32, self.dcallback)
		#rospy.spin()

	def xcallback(self,data):
		#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
			#global xarray
		#xarray=[]
		print 'len darray is ',len(self.darray)
		self.xarray.append(-1.0*data.data)
		if len(self.xarray)==10:
			self.plot()
		if len(self.xarray)==18:
			del self.xarray[:]
		
		#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ

	def dcallback(self,data):
		#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
		self.darray.append(-1*data.data)

		if len(self.darray)==18:
			del self.darray[:]

	def shutdown(self):
        # stop turtlebot
        	rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        #self.velocity_publisher.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
		rospy.sleep(1)


	def plot(self):
		print ('Hi')
		
		print 'bye'
		plt.plot(0,0,'*')
		plt.plot(self.xarray,self.darray)
		plt.xlabel('X values')
		plt.ylabel('Y values')
		plt.grid(True)
		plt.axis((-5,+5,-7,2))
		plt.savefig('/home/saeid/catkin_ws/src/doorBot/Plots/'+str(self.nowTime)+'.png')

def main():

	x=plotclass()
	rospy.spin()

if __name__=="__main__":
	main()