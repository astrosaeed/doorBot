#! /home/saeid/.virtualenvs/keras_tf/bin/python

from __future__ import division
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



def loadmodel(modelfile):
	model = load_model(modelfile)

	return model

def scaler(X, new_length):

	old_indices = np.arange(0,X.shape[0])
	
	new_indices = np.linspace(0,X.shape[0]-2,new_length)
	spl = UnivariateSpline(old_indices,X,k=3,s=0)
	new_array = spl(new_indices)
	new_array=new_array.reshape(-1, 1) 
	



	scaler = preprocessing.MinMaxScaler()
	array = scaler.fit_transform(new_array)
	array=array.reshape(1, -1) 
	
	return array

def handle_prediction(req):
	mymodel = loadmodel('/home/saeid/catkin_ws/src/doorBot/src/iter53.h5')
	X=np.asarray(req.a)
	Y=np.asarray(req.b)
	print X
	X=scaler(X,30)         #probably rnage of scaling should be same as training data
	Y=scaler(Y,30)
	print 'X shape is ',X.shape
	newarray=np.empty([1,2*X.shape[1]])  
	for i in range(X.shape[1]):
		newarray[0,2*i]=X[0,i]
		newarray[0,2*i+1]=Y[0,i]
	print 'new_array shape',newarray.shape
	newarray=newarray.reshape(newarray.shape[0],int((newarray.shape[1]/2)),2)
	predictions = mymodel.predict(newarray, verbose=1)
	binarizer = Binarizer(threshold=0.1).fit(predictions)
	binary1=binarizer.transform(predictions)
	print 
        del mymodel
	return binary1[0,0]


def main():

	rospy.init_node('predict')
	s = rospy.Service('predict', pred, handle_prediction)
	
	
	#mymodel = loadmodel('iter72.h5')
	
 #   X = getdata('pclx.txt')
 #   Y = getdata('pcld.txt')
	
	#X=scaler(X,76)         #probably rnage of scaling should be same as training data
	#Y=scaler(Y,76)
	#newarray=np.empty([1,2*X.shape[1]])  
	#for i in range(X.shape[1]):
	#    newarray[0,2*i]=X[0,i]
	#    newarray[0,2*i+1]=Y[0,i]
	
	
	#print handle_prediction(newarray)
	rospy.spin()	

if __name__=="__main__":

	main()
