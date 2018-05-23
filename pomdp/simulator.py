#!/usr/bin/env python
from parser import Policy
from pomdp_parser import Model

class Simulator:
	def __init__(self, pomdpfile='program.pomdp'):
		
		self.init_state=None
		self.b=[0.25, 0.25, 0.25, 0.25]
		self.model = Model(filename='program.pomdp', parsing_print_flag=True)
		self.policy = Policy(5,4 ,output='program.policy')
		self.a_idx=None

	

	#def update(self, a_idx, ):
	#		belief= T*O/normalizer

	def run(self):
		self.init_state=random(states)
		self.a_idx=policy.select_action(self.b)
		
	#	update(a_idx)

def main():

	Simulator()





if __name__=="__main__":
	main()