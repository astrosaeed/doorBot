#!/usr/bin/env python
from parser import Policy,Solver
from pomdp_parser import Model
import numpy as np
from random import randint
import random
from reason import Reason


class Simulator:
	def __init__(self, pomdpfile='program.pomdp'):
		
		
		
		self.model = Model(filename='program.pomdp', parsing_print_flag=False)
		self.policy = Policy(5,4 ,output='program.policy')
		print self.model.states		

	def init_belief(self):
			
		l = len(self.model.states)
		b = np.zeros(l)

		# initialize the beliefs of the states with index=0 evenly
		
		for i in range(l):
			b[i] = 1.0/l
			
		return b


	def get_state_index(self,state):

		return self.model.states.index(state)


	def init_state(self):
		state=random.choice(['not_forward_not_interested','not_forward_interested'])
		print state
		s_idx = self.get_state_index(state)
		print s_idx
		return s_idx, state

	def get_obs_index(self, obs):

		return self.model.observations.index(obs)

	

	def random_observe(self, a_idx):
		if self.model.actions[a_idx]=='move_forward':
			obs=random.choice(['physical','no_physical'])
		elif self.model.actions[a_idx]=='greet':
			obs=random.choice(['verbal','no_verbal'])
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
		
		b = [b[i] * self.model.obs_mat[a_idx, i, o_idx] for i in range(len(self.model.states))]
		
		b = b / sum(b)
		return b

	def run(self):
		s_idx,temp = self.init_state()
		b = self.init_belief()
		cost =0
		#print ( 'b shape is,', b.shape )
		#print b

		while True: 
			a_idx=self.policy.select_action(b)
			a = self.model.actions[a_idx]
		
			print('action selected',a)

			o_idx = self.random_observe(a_idx)
			#print ('transition matrix shape is', self.model.trans_mat.shape)
			#print self.model.trans_mat[a_idx,:,:]
			#print ('observation matrix shape is', self.model.obs_mat.shape)
			#print self.model.trans_mat[a_idx,:,:]
			print s_idx
			cost = cost + self.model.reward_mat[a_idx,s_idx]
			print ('Total reward is,' , cost)		
			b =self.update(a_idx,o_idx, b)
			print b
			success=0
			
			if 'report' in a:
				if 'not_interested' in a and 'not_interested' in temp:
					success= 1
					print 'Trial was successfull'
				elif 'report_interested' in a and 'forward_interested' in temp:
					success= 1
					print 'Trial was successful'
				print ('finished ')
				break

		return cost, success


	def trial_num(self, num):
		total_success=0
		total_cost=0
		for i in range(num):
			a,b=self.run()
			total_cost+=a
			total_success+=b

		print 'Average total reward is:', total_cost/num
		print 'Average total success is: ', float(total_success)/num

def main():
	Solver()
	a=Simulator()
	print a.trial_num(300)




if __name__=="__main__":
	main()