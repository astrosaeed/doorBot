'''
#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
xarray=[]
darray=[]
def xcallback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    xarray.append(data.data)
    print 'len xarray is ',len(xarray)

def dcallback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    darray.append(data.data)
    print 'len darray is ',len(darray)

	    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('saeid_node', anonymous=True)

    rospy.Subscriber("trajx_topic", Float32, xcallback)
    rospy.Subscriber("trajd_topic", Float32, dcallback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
'''