#!/usr/bin/env python
from parser import Policy
from pomdp_parser import Model
import numpy as np
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

	#def update(self, a_idx, ):
	#		belief= T*O/normalizer

	def run(self):
		#self.init_state=random(states)
		b=self.init_belief() 
		a_idx=self.policy.select_action(b)
		a = self.model.actions[a_idx]
		type(a)
		print('action selected',a)
		
	#	update(a_idx)

def main():

	a=Simulator()
	a.run()




if __name__=="__main__":
	main()