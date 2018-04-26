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
global xarray,darray
xarray=[]
darray=[]
def moveToGoal(xGoal,yGoal):
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



def predict_client(Xlist,Ylist):
	rospy.wait_for_service('predict')
	try:
		predict_list = rospy.ServiceProxy('predict', pred)
		#resp1 = add_list(x,y)
		resp = predict_list(Xlist, Ylist)
		return resp.pred
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e


def xcallback(data):
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        #global xarray
	#xarray=[]
	xarray.append(-1.0*data.data)
	cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	out = open('xvalues'+str(nowTime)+'.csv', 'a')
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
	if len(xarray)==15:
		print 'hello'
		Xlist=xarray
		Ylist=darray
		a = predict_client(Xlist, Ylist)
		print 'prediction is ',a
		#del xarray[:]
			
		if a==1:
			print('go forward')	
#			moveToGoal(humanx,humany)
			cmd_vel.publish(move_cmd)
	#print 'len xarray is ',len(xarray)
	if len(xarray)==16:
		del xarray[:]

def dcallback(data):
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
	darray.append(-1*data.data)
	out = open('yvalues.csv', 'a')

        temp=-1.0*float(data.data)
        out.write('%f,' % temp)
    	out.write('\n')
	out.close()
	print 'len darray is ',len(darray)

	if len(darray)==16:
		del darray[:]
def getdata(datafile):

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

def scaler(X, new_length):

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


def posecallback(data):
	global humanx
	global humany 	
	humanx=data.pose.position.x
	humany=data.pose.position.y


def listener():

	
	rospy.init_node('saeid_node', anonymous=True)
	global nowTime 
	nowTime=rospy.Time.now()

	rospy.Subscriber("trajx_topic", Float32, xcallback)
	rospy.Subscriber("trajd_topic", Float32, dcallback)
	rospy.Subscriber("segbot_pcl_person_detector/human_poses", PoseStamped, posecallback)
	
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()


def main():
		  
#	Xlist = getdata('pclx.txt')
#	Ylist = getdata('pcld.txt')
	listener()


	
	

if __name__=="__main__":

	main()
