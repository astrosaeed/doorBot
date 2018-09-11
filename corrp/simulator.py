#!/usr/bin/env python
from parser import Policy,Solver
from pomdp_parser import Model
import numpy as np
from random import randint
import random
from reason import Reason


class Simulator:
	def __init__(self, pomdpfile='program.pomdp'):
		
		self.time = ['morning','afternoon','evening']
		self.location = ['classroom','library']
		self.identity = ['student','professor','visitor'] 
		self.intention =['interested','not_interested']
		self.reason =Reason('reason.plog')
		#self.model = Model(filename='program.pomdp', parsing_print_flag=False)
		#self.policy = Policy(5,4 ,output='program.policy')
		#print self.model.states
	def sample (self, alist, distribution):

		return np.random.choice(alist, p=distribution)

	def create_instance(self):
		instance= []

		person = random.choice(self.identity)
		print ('sampled from identity with uniform prob distribution ')
		print ('identity is:'), person
		if person == 'student':
			place =self.sample(self.location,[0.4,0.6])
			time =self.sample(self.time,[0.4,0.4,0.2])
			intention =self.sample(self.intention,[0.3,0.7])
		elif person == 'professor':
			place =self.sample(self.location,[0.9,0.1])
			time =self.sample(self.time,[0.5,0.4,0.1])
			intention =self.sample(self.intention,[0.1,0.9])
		else:
			place = self.sample(self.location,[0.7,0.3])
			time =self.sample(self.time,[0.2,0.7,0.1])
			intention =self.sample(self.intention,[0.9,0.1])

		print ('based on identity, our instance is')
		
		instance.append(person)
		instance.append(time)
		instance.append(place)
		instance.append(intention)
		print (instance[0],instance[1],instance[2], instance[3])
		return instance


	def observe_fact(self):

		time = random.choice(self.time)
		location = random.choice (self.location)
		print ('observed time: '),time
		print ('observed location: '),location
		return time, location

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

	

	def update(self, a_idx,o_idx,b ):
		b = np.dot(b, self.model.trans_mat[a_idx, :])
		
		b = [b[i] * self.model.obs_mat[a_idx, i, o_idx] for i in range(len(self.model.states))]
		
		b = b / sum(b)
		return b

	def run(self):
		time, location =self.observe_fact() 	
		prob = self.reason.query_nolstm(time, location)
		print ('PROB is :'), prob
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
			tp=0
			tn=0
			fp=0
			fn=0
			
			if 'report' in a:
				if 'not_interested' in a and 'not_interested' in temp:
					success= 1
					tn=1
					print 'Trial was successfull'
				elif 'report_interested' in a and 'forward_interested' in temp:
					success= 1
					tp=1
					print 'Trial was successful'
				elif 'report_interested' in a and 'forward_not_interested' in temp:
					fp=1
					print 'Trial was unsuccessful'
				elif 'not_interested' in a and 'forward_interested' in temp:
					fn=1

				print ('finished ')
				break

		return cost, success, tp, tn, fp, fn


	def trial_num(self, num):
		total_success = 0
		total_cost = 0
		total_tp = 0
		total_tn = 0
		total_fp = 0
		total_fn = 0
		for i in range(num):
			c, s, tp, tn, fp, fn=self.run()
			total_cost+=c
			total_success+=s
			total_tp+=tp
			total_tn+=tn
			total_fp+=fp
			total_fn+=fn

		print 'Average total reward is:', total_cost/num
		print 'Average total success is: ', float(total_success)/num
		print 'Precision is ',float(total_tp)/(total_tp + total_fp)
		print 'Recall is ', float(total_tp)/(total_tp + total_fn)
def main():
	Solver()
	a=Simulator()
	a.run()




if __name__=="__main__":
	main()