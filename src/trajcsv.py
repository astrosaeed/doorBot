#!/usr/bin/env python

import rospy
import csv

from std_msgs.msg import Float32
import datetime

class plotclass:
	def __init__(self):
		
		rospy.init_node('traj_node', anonymous=True)
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
		
		self.xarray.append(-1.0*data.data)
		out = open('/home/saeid/catkin_ws/src/doorBot/Traj/'+str(self.nowTime)+'x.csv', 'a')
		temp=-1.0*float(data.data)
		out.write('%f,' % temp)
		out.write('\n')
		out.close()

		
		
		#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ

	def dcallback(self,data):
		#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
		self.darray.append(-1*data.data)
		out = open('/home/saeid/catkin_ws/src/doorBot/Traj/'+str(self.nowTime)+'y.csv', 'a')
		temp=-1.0*float(data.data)
		out.write('%f,' % temp)
		out.write('\n')
		out.close()

		

	def shutdown(self):
        # stop turtlebot
        	rospy.loginfo("Stop TurtleBot")

		rospy.sleep(1)



		
		
		

def main():

	x=plotclass()
	rospy.spin()

if __name__=="__main__":
	main()