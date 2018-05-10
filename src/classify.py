#! /home/saeid/.virtualenvs/keras_tf/bin/python
from __future__ import division
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from doorBot.srv import *
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist,PoseStamped
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
import csv
import sys
import roslib; roslib.load_manifest('sound_play')
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from collections import deque
from keras.models import Sequential 
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from keras.models import Model
from keras.layers import Input, Embedding,Dense
from sklearn.model_selection import train_test_split                #useful for splitting data into training and test sets
from sklearn import preprocessing
from sklearn.preprocessing import Binarizer
#import metric
import glob
from keras.preprocessing import sequence
import pandas as pd
import numpy as np
#import customscale as cs
from keras.models import load_model
import openpyxl
import xlsxwriter
import xlrd
from numpy import *
from pandas import ExcelFile
from scipy.interpolate import UnivariateSpline

#from addlist.msg import foo
import rospy
from doorBot.srv import *
from doorBot.msg import my_msgs
class classify:
	def __init__(self):
		rospy.init_node('saeid_node', anonymous=True)

		#rospy.Subscriber("trajx_topic", Float32, self.xcallback)
		#rospy.Subscriber("trajd_topic", Float32, self.dcallback)
		rospy.Subscriber("traj_topic", my_msgs, self.callback)
		rospy.Subscriber("segbot_pcl_person_detector/human_poses", PoseStamped, self.posecallback)
		self.mymodel=load_model('/home/saeid/catkin_ws/src/doorBot/src/iter53.h5')
		self.detected=False
		soundhandle=SoundClient()
		s='How can I help you?'
		self.xarray=deque(15*[0], 15)
		self.darray=deque(15*[0], 15)
		self.flag=False
		self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		self.r=rospy.Rate(50)
		self.move_cmd = Twist()
		self.move_cmd.linear.x = 0.1
		self.move_cmd.angular.z = 0

		while not rospy.is_shutdown():
			#if len(self.xarray)==15:
			while self.detected:
				rospy.loginfo("Human Detected")
				Xlist=self.xarray
				Ylist=self.darray

				X=np.asarray(Xlist)
				Y=np.asarray(Ylist)
				print X 
				X=self.scaler(X,30)         #probably rnage of scaling should be same as training data
				Y=self.scaler(Y,30)
				print 'X shape is ',X.shape
				newarray=np.empty([1,2*X.shape[1]])  
				for i in range(X.shape[1]):
					newarray[0,2*i]=X[0,i]
					newarray[0,2*i+1]=Y[0,i]
				print 'new_array shape',newarray.shape
				newarray=newarray.reshape(newarray.shape[0],int((newarray.shape[1]/2)),2)
				predictions = self.mymodel.predict(newarray, verbose=1)
				binarizer = Binarizer(threshold=0.1).fit(predictions)
				binary1=binarizer.transform(predictions)
				print 'prediction is ',binary1
				if binary1==1:
					soundhandle.say(s)
					print('go forward')	
#					self.moveToGoal(humanx,humany)
					self.cmd_vel.publish(self.move_cmd)
					self.detected=False

					self.xarray=deque(15*[0], 15)
					self.darray=deque(15*[0], 15)
				elif binary1==0:
					self.detected=False
				 
			self.r.sleep()
            		
	    	
	def moveToGoal(self,xGoal,yGoal):
        	ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        	while(not ac.wait_for_server(rospy.Duration.from_sec(5.0))):
            		rospy.loginfo("Waiting for move_base action server to respond")

        	goal = MoveBaseGoal()

        	goal.target_pose.header.frame_id = "map"
        	goal.target_pose.header.stamp = rospy.Time.now()

        	goal.target_pose.pose.position = Point(xGoal,yGoal,0)
        	goal.target_pose.pose.orientation.x = 0.0
        	goal.target_pose.pose.orientation.y = 0.0
        	goal.target_pose.pose.orientation.z = 0.0
        	goal.target_pose.pose.orientation.w = 1.0
        	rospy.loginfo("Sending goal...")
        	ac.send_goal(goal)

        	ac.wait_for_result(rospy.Duration(20))

	
	def scaler(self,X, new_length):

		old_indices = np.arange(0,X.shape[0])
	
		new_indices = np.linspace(0,X.shape[0]-2,new_length)
		spl = UnivariateSpline(old_indices,X,k=3,s=0)
		new_array = spl(new_indices)
		new_array=new_array.reshape(-1, 1) 

		scaler = preprocessing.MinMaxScaler()
		array = scaler.fit_transform(new_array)
		array=array.reshape(1, -1) 
	
		return array
	def shutdown(self):
        	rospy.loginfo("Stop SegBot")
		rospy.sleep(1)

	def callback(self, data):
		#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        	#global xarray
		#xarray=[]
		self.xarray.append(-1.0*data.x)
		self.darray.append(-1.0*data.y)

		self.detected=True	
		r = rospy.Rate(30);

	'''
	def xcallback(self, data):
		#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        	#global xarray
		#xarray=[]
		self.xarray.append(-1.0*data.data)
		self.detected=True	
		r = rospy.Rate(10);

		
		
	#print 'len xarray is ',len(xarray)
		if len(self.xarray)==20:
			del self.xarray[:]

	def dcallback(self, data):
		#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
		self.darray.append(-1*data.data)

		if len(self.darray)==20:
			del self.darray[:]
	'''
	def getdata(self,datafile):

		fd=open(datafile, 'r')
		d = fd.readlines()
		fd.close()
	
	#myarray=np.zeros((len(d) -1,1))
		mylist=[]
		for i in range(1,len(d)):

		#myarray[i-1,0]= float(d[i])
			mylist.append(float(d[i]))
	
#    return myarray
		return mylist

	def scaler(self,X, new_length):

		old_indices = np.arange(0,X.shape[0])
	
		new_indices = np.linspace(0,X.shape[0]-2,new_length)
		spl = UnivariateSpline(old_indices,X,k=3,s=0)
		new_array = spl(new_indices)
		new_array=new_array.reshape(-1, 1) 
		#print 'new_array', new_array



		scaler = preprocessing.MinMaxScaler()
		array = scaler.fit_transform(new_array)
		array=array.reshape(1, -1) 
	
		return array


	def posecallback(self,data):
		global humanx
		global humany 	
		humanx=data.pose.position.x
		humany=data.pose.position.y




def main():
		  
	classify()

	ros.spin()
	
	

if __name__=="__main__":

	main()
