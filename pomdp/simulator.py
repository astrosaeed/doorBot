#!/usr/bin/env python
from parser import Policy
from pomdp_parser import Model
import numpy as np
from random import randint
import random


class Simulator:
	def __init__(self, pomdpfile='program.pomdp'):
		
		self.init_state=None
		
		self.model = Model(filename='program.pomdp', parsing_print_flag=False)
		self.policy = Policy(5,4 ,output='program.policy')
		

	def init_belief(self):
		l = len(self.model.states)
		b = np.zeros(l)

		# initialize the beliefs of the states with index=0 evenly
		
		for i in range(l):
			b[i] = 1.0/l
			
		return b


	def get_obs_index(self, obs):

		return self.model.observations.index(obs)

	def random_observe(self, a_idx):
		if self.model.actions[a_idx]=='move_forward':
			obs=random.choice(['physical','no_physical','na'])
		elif self.model.actions[a_idx]=='greet':
			obs=random.choice(['verbal','no_verbal','na'])
		else:
			obs = 'na'
		#l=len(self.model.observations)-1
		#o_idx=randint(0,l)
		o_idx=self.get_obs_index(obs)
		print ('random observation is: ',self.model.observations[o_idx])
		return o_idx

	
	#def update(self, a_idx,o_idx,b ):
	#	temp = np.matmul(self.model.trans_mat[0,:,:],self.model.obs_mat[0,:,:])
	#	temp = np.matmul(b,temp)
	#	b = temp/np.sum(temp)
	#	return b

	def update(self, a_idx,o_idx,b ):
		b = np.dot(b, self.model.trans_mat[a_idx, :])
		print b
		b = [b[i] * self.model.obs_mat[a_idx, i, o_idx] for i in range(len(self.model.states))]
		print b
		b = b / sum(b)
		return b

	def run(self):
		#self.init_state=random(states)
		b=self.init_belief()
		print ( 'b shape is,', b.shape )
		print b

		for i in range(1): 
			a_idx=self.policy.select_action(b)
			a = self.model.actions[a_idx]
		
			print('action selected',a)

			o_idx = self.random_observe(a_idx)
			#print ('transition matrix shape is', self.model.trans_mat.shape)
			#print self.model.trans_mat[a_idx,:,:]
			#print ('observation matrix shape is', self.model.obs_mat.shape)
			#print self.model.trans_mat[a_idx,:,:]
		
			b =self.update(a_idx,o_idx, b)
			print b

def main():

	a=Simulator()
	a.run()




if __name__=="__main__":
	main()