import csv
import numpy as np
import random
from keras.models import load_model

class Learning:
	def __init__(self, path,filenamex,filenamey):

		self.path=path
		self.xdata = np.genfromtxt(path+filenamex, delimiter=',')
		self.ydata = np.genfromtxt(path+filenamey, delimiter=',')
		self.mymodel=load_model('./iter53.h5')

	def get_traj(self):
		(m,n)=self.xdata.shape
		randrow=random.randint(0,m)
		randrow_label=self.xdata[randrow,n-1]
		extractx=self.xdata[randrow, n-1-30:n-1]
		label= self.xdata[randrow, n-1]
		extracty=self.ydata[randrow, n-1-30:n-1]
		extractx=extractx.reshape(1,-1)
		extracty=extracty.reshape(1,-1)
		print extractx.shape, label

		#self.ydata = np.genfromtxt(path+filenamey, delimiter=',')
		(p,q)=self.ydata.shape

		
		newarray=np.empty([1,2*extractx.shape[1]])
		for i in range(extractx.shape[1]):
					newarray[0,2*i]=extractx[0,i]
					newarray[0,2*i+1]=extracty[0,i]
		print 'new_array shape',newarray.shape
		newarray=newarray.reshape(newarray.shape[0],int((newarray.shape[1]/2)),2)
		return newarray, label

	def	predict(self, newarray):
		predictions = self.mymodel.predict(newarray, verbose=1)
		print predictions
		return predictions

def main():

	a=Learning('./','interposx.csv','interposy.csv')



if __name__=='__main__':
	main()
