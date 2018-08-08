from reason import Reason
from simulator import Simulator	
import numpy as np
from parser import Policy,Solver
from pomdp_parser import Model
from random import randint
import random

class Corrp():

	def __init__(self,pomdpfile='program.pomdp'):
		#self.obj=Reason()
		
		
		self.obj = None
		self.model = Model(filename='program.pomdp', parsing_print_flag=False)
		self.policy = Policy(5,4 ,output='program.policy')
		print self.model.states
		self.decision= None
		self.time = None
		self.location = None
		self.suplearn= None

	def init_belief(self):        #remember later to change it to override method
		self.obj=Reason()
		time = ['(currenttime=morning)', '(currenttime=afternoon)', '(currenttime=evening)']
		location = ['(atlocation=classroom)','(atlocation=library)']
		lstm = ['(classifier=zero)','(classifier=one)']
		decision = ['interested', 'not_interested']
		

		time_rand = random.choice(time)
		loc_rand = random.choice(location)
		lstm_rand = random.choice(lstm)


		int_prob= float(self.obj.query_nolstm('reason_nolstm.plog',self.decision, time_rand, loc_rand))
	
		self.obj.delete('reason_nolstm.plog')
		print int_prob
		
		init_belief = [1.0 - int_prob, int_prob, 1.0 - int_prob, int_prob, 0]
		b = np.zeros(len(init_belief))
		for i in range(len(init_belief)):
			b[i] = init_belief[i]/sum(init_belief)

		print b
		return b

	def init_state(self):
		#state=random.choice(['not_forward_not_interested','not_forward_interested'])
		self.decision =random.choice(['interested','not_interested'])
		print 'the random decision is:', self.decision
		self.time=random.choice(['morning','afternoon', 'evening'])
		print 'The random time is ', self.time
		self.location=random.choice(['library','classroom'])
		print 'The random location is : ', self.location
		
		
			
 

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

	def observe_logical(self, a_idx):
		if self.model.actions[a_idx]=='move_forward' and self.decision == 'interested':
			obs='physical'
		elif self.model.actions[a_idx]=='move_forward' and self.decision == 'not_interested':
			obs='no_physical'
		elif self.model.actions[a_idx]=='greet' and self.decision == 'interested':
			obs='verbal'
		elif self.model.actions[a_idx]=='greet' and self.decision == 'not_interested':
			obs='no_verbal'
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



	def lstm(self):
		pred = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
		#pred_int = [0.9,1.0]
		#pred_not_int = [0.0,0.1,0.2]
		if random.choice(pred) >= 0.5:
			self.suplearn = 1
			self.classifier = 'one'
		else:
			self.suplearn = 0
			self.classifier = 'zero'
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
			#o_idx= self.observe_logical(a_idx)
			#print ('transition matrix shape is', self.model.trans_mat.shape)
			#print self.model.trans_mat[a_idx,:,:]
			#print ('observation matrix shape is', self.model.obs_mat.shape)
			#print self.model.trans_mat[a_idx,:,:]
			print s_idx
			cost = cost + self.model.reward_mat[a_idx,s_idx]
			print ('Total reward is,' , cost)		
			b =self.update(a_idx,o_idx, b)
			print b
			success = 0
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

		return cost, success,  tp, tn, fp, fn


	def trial_num(self, num):
		total_success=0
		total_cost=0
		total_tp = 0
		total_tn = 0
		total_fp = 0
		total_fn = 0

		for i in range(num):
			random.seed(i)
			c,s, tp, tn, fp, fn=self.run()
			total_cost+=c
			total_success+=s
			total_tp+=tp
			total_tn+=tn
			total_fp+=fp
			total_fn+=fn

		print 'Average total reward is:', total_cost/num
		print 'Average total success is: ', float(total_success)/num
		Precision = float(total_tp)/(total_tp + total_fp)
		print 'Precision is ', Precision
		Recall = float(total_tp)/(total_tp + total_fn)
		print 'Recall is ', Recall
		F1score = 2.0*Precision*Recall/(Precision + Recall)
		print 'F1 score', F1score



def main():
	a = Corrp()
	a.trial_num(200)






if __name__ == "__main__":

	main()	