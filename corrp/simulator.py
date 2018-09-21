#!/usr/bin/env python
from parser import Policy,Solver
from pomdp_parser import Model
import numpy as np
from random import randint
import random
from reason import Reason
from learning import Learning

class Simulator:
	def __init__(self, pomdpfile='program.pomdp'):
		
		self.time = ['morning','afternoon','evening']
		self.location = ['classroom','library']
		self.identity = ['student','professor','visitor'] 
		self.intention =['interested','not_interested']
		self.reason =Reason('reason.plog')
		self.model = Model(filename='program.pomdp', parsing_print_flag=False)
		self.policy = Policy(5,4 ,output='program.policy')
		self.instance = []
		self.results={}
		self.learning=Learning('./','interposx.csv','interposy.csv')
		self.trajectory_label=0

	def sample (self, alist, distribution):

		return np.random.choice(alist, p=distribution)

	def create_instance(self):
		

		person = random.choice(self.identity)
		print ('\nLet\'s uniformly sample from [student, visitor, professor] : '), person
#		print ('identity is:'), person
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
		self.trajectory_label = self.learning.get_traj()

		print ('Given the probabilty distribution for '+person+', we sample from time, location and intention.')
		
		self.instance.append(person)
		self.instance.append(time)
		self.instance.append(place)
		self.instance.append(intention)
		self.instance.append('trajectory with label '+str(self.trajectory_label))
		print ('Our instance would be (trajectory will be added soon): ')
		print (self.instance[0],self.instance[1],self.instance[2], self.instance[3],self.instance[4])
		return self.instance


	def observe_fact(self):
		print '\nNow, we randomly (uniform) make observations of time and location:'
		time = self.instance[1]
		location = self.instance[2]
		print ('observed time: '),time
		print ('observed location: '),location
		return time, location

	def init_belief(self, int_prob):
			
		l = len(self.model.states)
		b = np.zeros(l)

		# initialize the beliefs of the states with index=0 evenly
		
		int_prob =float(int_prob)
		init_belief = [1.0 - int_prob, int_prob, 0, 0, 0]
		b = np.zeros(len(init_belief))
		for i in range(len(init_belief)):
			b[i] = init_belief[i]/sum(init_belief)
		print 'The normalized initial belief would be: '
		print b
		return b
			
		return b


	def get_state_index(self,state):

		return self.model.states.index(state)


	def init_state(self):
		state=random.choice(['not_forward_not_interested','not_forward_interested'])
		print 'Randomly selected state from [not_forward_not_interested,not_forward_interested] =',state
		s_idx = self.get_state_index(state)
		#print s_idx
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

	def run(self, strategy,time,location):
		#self.create_instance()
		#time, location =self.observe_fact()	
		
		#print ('PROB is :'), prob
		success=0
		tp=0
		tn=0
		fp=0
		fn=0
		cost =0

		if strategy == 'corrp':
			prob = self.reason.query_nolstm(time, location)
			print '\nOur POMDP Model states are: '
			print self.model.states

			s_idx,temp = self.init_state()
			b = self.init_belief(prob)
			
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
				#print s_idx
				cost = cost + self.model.reward_mat[a_idx,s_idx]
				print ('Total reward is,' , cost)		
				b =self.update(a_idx,o_idx, b)
				print b
				
				
				if 'report' in a:
					if 'not_interested' in a and 'not_interested' == self.instance[3]:
						success= 1
						tn=1
						print 'Trial was successfull'
					elif 'report_interested' in a and 'interested' == self.instance[3]:
						success= 1
						tp=1
						print 'Trial was successful'
					elif 'report_interested' in a and 'not_interested' == self.instance[3]:
						fp=1
						print 'Trial was unsuccessful'
					elif 'not_interested' in a and 'interested' == self.instance[3]:
						fn=1

					print ('Finished\n ')
					
					break

		if strategy == 'reasoning':
			prob = self.reason.query_nolstm(time, location,'reason_nolstm.plog')
			print '\n Strategy is: ', strategy
			print 'RECAP: our instance is: '
			print self.instance
			print ('RECAP:observed time: '),time
			print ('RECAP:observed location: '),location
			print ('probability of person being ineterested given the observed facts: '), prob
			threshold = 0.5
			prob=float(prob)
			if prob>= threshold and 'interested' == self.instance[3] :
				success = 1
				print ('This probability is greater than threshold ='+str(threshold)+', therefore reasoner says human HAS intention')
				print 'Trial was successful'
				tp=1
			elif prob>= threshold and 'not_interested' == self.instance[3]:
				success=0
				fp=1
				print ('This probability is greater than threshold ='+str(threshold)+', therefore reasoner says human HAS intention')
				print 'Trial was unsuccessful'
			elif prob < threshold and 'interested' == self.instance[3] :
				success = 0
				print ('This probability is less than threshold ='+str(threshold)+', therefore reasoner says human does NOT HAVE intention')
				fn=1
				print 'Trial was unsuccessful'
			else:
				success = 1
				print ('This probability is less than threshold ='+str(threshold)+', therefore reasoner says human does NOT HAVE intention')
				print 'Trial was successful'
				tn=1

		if strategy=='learning':
			
			res = self.learning.predict()
			if res>0.5 and self.trajectory_label ==1.0:
				print ('CASE I the trajectory shows person is interested')
				success=1
				tp=1
			elif res<0.5 and self.trajectory_label ==0:
				
				print ('CASE II the person is not interested')
				success =1
				tn=1
			elif res>0.5 and self.trajectory_label ==0:
				sucess=0
				fp =1
				print ('CASE III the trajectory shows person is interested')
			elif res <0.5 and self.trajectory_label == 1.0:
				fn =1
				success =0
				('CASE IV the person is not interested')
		


		if strategy =='lcorrp':
			res = self.learning.predict()
			if res > 0.5:
				prob = self.reason.query(time, location,'one','reason.plog')
			else:
				prob = self.reason.query(time, location,'zero','reason.plog')
			print '\nOur POMDP Model states are: '
			print self.model.states
			print 'bye'
			s_idx,temp = self.init_state()
			b = self.init_belief(prob)
			
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
				#print s_idx
				cost = cost + self.model.reward_mat[a_idx,s_idx]
				print ('Total reward is,' , cost)		
				b =self.update(a_idx,o_idx, b)
				print b
				
				
				if 'report' in a:
					if 'not_interested' in a and self.trajectory_label == 0:
						success= 1
						tn=1
						print 'Trial was successfull'
					elif 'report_interested' in a and self.trajectory_label == 1:
						success= 1
						tp=1
						print 'Trial was successful'
					elif 'report_interested' in a and self.trajectory_label == 0:
						fp=1
						print 'Trial was unsuccessful'
					elif 'not_interested' in a and self.trajectory_label == 1:
						fn=1

					print ('Finished\n ')
					
					break
						
		return cost, success, tp, tn, fp, fn


	def trial_num(self, num,strategylist):
		total_success = {}
		total_cost = {}
		total_tp = {}
		total_tn = {}
		total_fp = {}
		total_fn = {}

		for strategy in strategylist:
			total_success[strategy] = 0
			total_cost[strategy] = 0
			total_tp[strategy]= 0
			total_tn[strategy]= 0
			total_fp[strategy]= 0
			total_fn[strategy]= 0

		for i in range(num):
			self.create_instance()
			time, location =self.observe_fact()
			for strategy in strategylist:
				#random.seed(i)
				c, s, tp, tn, fp, fn=self.run(strategy,time,location)
				total_cost[strategy]+=c
				total_success[strategy]+=s
				total_tp[strategy]+=tp
				total_tn[strategy]+=tn
				total_fp[strategy]+=fp
				total_fn[strategy]+=fn

			self.instance =[]
		for strategy in strategylist:
			print 'Average total reward for '+strategy+'  is:', total_cost[strategy]/num
			print 'Average total success for '+strategy+'  is: ', float(total_success[strategy])/num
			try:
				print 'Precision for '+strategy+' is ',float(total_tp[strategy])/(total_tp[strategy] + total_fp[strategy])
				print 'Recall for '+strategy+' is ', float(total_tp[strategy])/(total_tp[strategy] + total_fn[strategy])
				self.results[strategy]= [total_cost[strategy]/num,float(total_success[strategy])/num,float(total_tp[strategy])/(total_tp[strategy] + total_fp[strategy]), float(total_tp[strategy])/(total_tp[strategy] + total_fn[strategy])]
			except:
				print 'Can not divide by zero'
				self.results[strategy]= [total_cost[strategy]/num,float(total_success[strategy])/num,'N/A', 'N/A']

	def print_results(self):
		print '\n WRAP UP OF RESULTS:'
		print self.results


def main():
	#strategy = ['corrp', 'reasoning','learning','lcorrp']
	strategy = ['reasoning']
	print 'startegies are:', strategy
	Solver()
	a=Simulator()
	
	num=5
	a.trial_num(num,strategy)
	a.print_results()



if __name__=="__main__":
	main()