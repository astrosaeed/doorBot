#! /home/saeid/.virtualenvs/keras_tf/bin/python


import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from doorBot.srv import *
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist,PoseStamped
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
import csv


class myclass:
	def __init__(self):
		rospy.init_node('saeid_node', anonymous=True)
		self.xarray=[]
		self.darray=[]
		self.humanx=None
		self.humany=None
		self.nowTime=rospy.Time.now() 
	

		rospy.Subscriber("trajx_topic", Float32, self.xcallback)
		rospy.Subscriber("trajd_topic", Float32, self.dcallback)
		rospy.Subscriber("segbot_pcl_person_detector/human_poses", PoseStamped, self.posecallback)
		rospy.spin()

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



	def predict_client(self,Xlist,Ylist):
		rospy.wait_for_service('predict')
		try:
			predict_list = rospy.ServiceProxy('predict', pred)
			#resp1 = add_list(x,y)
			resp = predict_list(Xlist, Ylist)
			return resp.pred
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e


	def xcallback(self,data):
		#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
			#global xarray
		#xarray=[]
		self.xarray.append(-1.0*data.data)
		cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		out = open('xvalues'+str(self.nowTime)+'.csv', 'a')
		temp=-1.0*float(data.data)
		out.write('%f,' % temp)
		out.write('\n')
		out.close()
		#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
		r = rospy.Rate(10);

			# Twist is a datatype for velocity
		move_cmd = Twist()
		# let's go forward at 0.2 m/s
		move_cmd.linear.x = 0.1
		# let's turn at 0 radians/s
		move_cmd.angular.z = 0
		#a=raw_input()
		# as long as you haven't ctrl + c keeping doing...
		if len(self.xarray)==15:
			print 'hello'
			Xlist=self.xarray
			Ylist=self.darray
			a = predict_client(Xlist, Ylist)
			print 'prediction is ',a
			#del xarray[:]
				
			if a==1:
				print('go forward')	
	#			moveToGoal(humanx,humany)
				cmd_vel.publish(move_cmd)
		#print 'len xarray is ',len(xarray)
		if len(self.xarray)==16:
			del self.xarray[:]

	def dcallback(self,data):
		#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
		self.darray.append(-1*data.data)
		out = open('yvalues.csv', 'a')

		temp=-1.0*float(data.data)
		out.write('%f,' % temp)
		out.write('\n')
		out.close()
		print 'len darray is ',len(self.darray)

		if len(self.darray)==16:
			del self.darray[:]

	def getdata(self, datafile):

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
			
		self.humanx=data.pose.position.x
		self.humany=data.pose.position.y



def main():
		  
	myclass()
	
	

if __name__=="__main__":

	main()
