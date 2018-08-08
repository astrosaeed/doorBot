from reason import Reason
from simulator import Simulator	
import numpy as np
from parser import Policy,Solver
from pomdp_parser import Model
from random import randint
import random

class Corrp():

	def __init__(self):
		#self.obj=Reason()
		
		
		self.obj = None
		
		self.decision= None
		self.time = None
		self.location = None
		self.suplearn= None

	def init_pred(self):        #remember later to change it to override method
		self.obj=Reason()
		time = ['(currenttime=rush)', '(currenttime=break)']
		location = ['(atlocation=at_entrance)','(atlocation=at_exit)']
		lstm = ['(classifier=zero)','(classifier=one)']
		decision = ['interested', 'not_interested']

		time_rand = random.choice(time)
		loc_rand = random.choice(location)
		lstm_rand = random.choice(lstm)


		int_prob= float(self.obj.query('reason.plog',self.decision, time_rand,lstm_rand, loc_rand))
	
		self.obj.delete('reason.plog')
		print int_prob
		
		print int_prob
		return int_prob

	def init_state(self):
		
		self.decision =random.choice(['interested','not_interested'])
		print 'the random decision is:', self.decision
		self.time=random.choice(['break','rush'])
		print 'The random time is ', self.time
		self.location=random.choice(['at_entrance','at_exit'])
		print 'The random location is : ', self.location
		self.lstm()
		
		print 'The classifier output is: ', self.classifier	
 

		return self.decision

	def get_state_index(self,state):

		return self.model.states.index(state)

	def get_obs_index(self, obs):

		return self.model.observations.index(obs)


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

		init = self.init_state()
		prob = self.init_pred()
		cost = 0
		#print ( 'b shape is,', b.shape )
		#print b

		
	
		success = 0
		tp=0
		tn=0
		fp=0
		fn=0
			
		if prob > 0.5:
			if 'interested' ==init:
				success= 1
				tp=1
				print 'Trial was successfull'
			elif 'not_interested' == init:
				success= 0
				fp=1
				print 'Trial was unsuccessful'
		else: 
			if 'not_interested' == init:
				tn=1
				success = 1
				print 'Trial was successful'
			elif 'interested' == init:
				fn=1

		#print ('finished ')
				

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
	a.trial_num(300)






if __name__ == "__main__":

	main()	