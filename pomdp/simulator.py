#!/usr/bin/env python
from parser import Policy
from pomdp_parser import Model
import numpy as np
from random import randint


class Simulator:
	def __init__(self, pomdpfile='program.pomdp'):
		
		self.init_state=None
		
		self.model = Model(filename='program.pomdp', parsing_print_flag=True)
		self.policy = Policy(5,4 ,output='program.policy')
		

	def init_belief(self):
		l = len(self.model.states)
		b = np.zeros(l)

		# initialize the beliefs of the states with index=0 evenly
		
		for i in range(l):
			b[i] = 1.0/l
			
		return b

	def random_observe(self):
		l=len(self.model.observations)-1
		o_idx=randint(0,l)
		print ('random observation is: ',self.model.observations[o_idx])
		return o_idx

#	def update(self, a_idx,o_idx,b ):
#			belief= T*O/normalizer

	def run(self):
		#self.init_state=random(states)
		b=self.init_belief()
		print ( 'b shape is,', b.shape )
		print b 
		a_idx=self.policy.select_action(b)
		a = self.model.actions[a_idx]
		
		print('action selected',a)
		o_idx = self.random_observe()
		print ('transition matrix shape is', self.model.trans_mat.shape)
		print self.model.trans_mat[0,:,:]
		print ('observation matrix shape is', self.model.obs_mat.shape)
#		update(a_idx,o_idx, b)

def main():

	a=Simulator()
	a.run()




if __name__=="__main__":
	main()