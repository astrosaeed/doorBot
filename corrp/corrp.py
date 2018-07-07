from reason import Reason
from simulator import Simulator	
import numpy as np
from parser import Policy,Solver
from pomdp_parser import Model
from random import randint
import random

class Corrp():

	def __init__(self,pomdpfile='program.pomdp'):
		self.obj=Reason()
		self.model = Model(filename='program.pomdp', parsing_print_flag=False)
		self.policy = Policy(5,4 ,output='program.policy')
		print self.model.states
		self.decision =random.choice(['interested','not_interested'])
		self.time=random.choice(['break','rush'])
		self.location=random.choice(['at_entrance','at_exit'])
	def init_belief(self):        #remember later to change it to override method
		int_prob =float( self.obj.query('reason.plog',self.decision,self.time,self.location,'currenttime=break') )
		self.obj.delete('reason.plog')
		print int_prob
		init_belief = [int_prob, 1.0-int_prob, int_prob, 1.0-int_prob, 0]
		b = np.zeros(len(init_belief))
		for i in range(len(init_belief)):
			b[i] = init_belief[i]/sum(init_belief)

		print b
		return b

	def init_state(self):
		#state=random.choice(['not_forward_not_interested','not_forward_interested'])
		if self.decision == 'interested':		
			state=random.choice(['not_forward_interested','forward_interested'])
		else:
			state = random.choice(['not_forward_not_interested','forward_not_interested'])
		print state
		s_idx = self.get_state_index(state)
		print s_idx
		return s_idx, state

	def get_state_index(self,state):

		return self.model.states.index(state)

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
	a=Corrp()
	a.trial_num(200)






if __name__ == "__main__":

	main()	