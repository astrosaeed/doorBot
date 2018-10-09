#!/usr/bin/env python
from parser import Policy,Solver
from pomdp_parser import Model
import numpy as np
from random import randint
import random
random.seed()
from reason import Reason
from learning import Learning
from simulator import Simulator
import pandas as pd


class Exp(Simulator):

	def observe_fact(self,i, acc_prec):
		random.seed(i)
		print '\nObservations:'
		time_local = self.time 
		location_local = self.location
		ind_time = time_local.index(self.instance[1])
		ind_location = location_local.index(self.instance[2])
		p_time = [0.0, 0.0, 0.0] 
		p_time[ind_time] = acc_prec
		print 'acc_prec', acc_prec
		for i in range(len(p_time)):

			if p_time[i]==0.0:
				p_time[i]=(1- acc_prec)/2.0
		print p_time		
		p_location = [0.0, 0.0]
		p_location[ind_location] = acc_prec
		for i in range(len(p_location)):
			if p_location[i]==0.0:
				p_location[i]=(1- acc_prec)/1.0


		time = self.sample(time_local,p_time)
		location = self.sample(location_local,p_location)
		print ('Observed time: '),time
		print ('Observed location: '),location
		return time, location



	def run(self, strategy,time,location):
	
		success=0
		tp=0
		tn=0
		fp=0
		fn=0
		cost =0

		if strategy == 'corrp':
			prob = self.reason.query_nolstm(time, location,'reason_nolstm.plog')
			print '\nStrategy is: ',strategy
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

				o_idx = self.observe(a_idx,self.instance[3])
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



		if strategy == 'planning':
			#prob = self.reason.query_nolstm(time, location,'reason_nolstm.plog')
			print '\nStrategy is: ',strategy
			print '\nOur POMDP Model states are: '
			print self.model.states

			s_idx,temp = self.init_state()
			init_belief = [0.25, 0.25, 0.25, 0.25, 0]
			b = np.zeros(len(init_belief))
			for i in range(len(init_belief)):
				b[i] = init_belief[i]/sum(init_belief)
			#b = self.init_belief(prob)
			
			#print ( 'b shape is,', b.shape )
			#print b

			while True: 
				a_idx=self.policy.select_action(b)
				a = self.model.actions[a_idx]
			
				print('action selected',a)

				o_idx = self.observe(a_idx,self.instance[3])
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
			print '\nStrategy is: ',strategy
			prob = self.reason.query_nolstm(time, location,'reason_nolstm.plog')
			#print 'RECAP: our instance is: '
			#print self.instance
			#print ('RECAP:observed time: '),time
			#print ('RECAP:observed location: '),location
			print ('P(ineterested)| observed time and location: '), prob
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


		if strategy =='lcorrp':
			print '\nStrategy is: ',strategy
			res = self.learning.predict()
			if res > 0.2:
				prob = self.reason.query(time, location,'one','reason.plog')
			else:
				prob = self.reason.query(time, location,'zero','reason.plog')
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

				o_idx = self.observe(a_idx,self.instance[3])
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

		if strategy =='lreasoning':
			print '\nStrategy is: ',strategy
			res = self.learning.predict()
			if res > 0.2:
				prob = self.reason.query(time, location,'one','reason.plog')
			else:
				prob = self.reason.query(time, location,'zero','reason.plog')
			threshold = 0.2
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

						
		return cost, success, tp, tn, fp, fn

	def trial_num(self, num,strategylist,acc_prec_dist):
		dflist=[]
		for j in range(len(acc_prec_dist)):
			dflist.append(pd.DataFrame())
		 
		
			for strategy in strategylist:
				total_success = 0
				total_cost = 0
				total_tp= 0
				total_tn= 0
				total_fp= 0
				total_fn= 0

				for i in range(num):
					self.create_instance(i)
					time, location =self.observe_fact(i,acc_prec_dist[j])
				
					
					
					c, s, tp, tn, fp, fn=self.run(strategy,time,location)
		
					total_cost+=c
					total_success+=s
					total_tp+=tp
					total_tn+=tn
					total_fp+=fp
					total_fn+=fn

				print ('total_tp:'), total_tp
				
				try:
					dflist[j].at[strategy,'Cost']= float(total_cost)/num
					dflist[j].at[strategy,'Success']= float(total_success)/num
					prec = round(float(total_tp)/(total_tp + total_fp),2)
					recall = round(float(total_tp)/(total_tp + total_fn),2)
					dflist[j].at[strategy,'Precision'] = prec 
					dflist[j].at[strategy,'Recall'] = recall 
					dflist[j].at[strategy,'F1 Score']= round(2*prec*recall/(prec+recall),2)
				
				except:
					print 'Can not divide by zero'
					dflist[j].at[strategy,'Precision']= 0
					dflist[j].at[strategy,'Recall']= 0
					dflist[j].at[strategy,'F1 Score']= 0
				
			
				self.instance =[]
		return dflist
		
		

	def print_results(self,dflist):
		print '\nWRAP UP OF RESULTS:'
		print dflist[0]
		print dflist[1]
	

	



def main():
	strategy = ['reasoning','lreasoning','planning','corrp','lcorrp']
	#strategy = ['lcorrp']
	print 'startegies are:', strategy
	Solver()
	a=Exp()
	acc_prec_dist= [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
	num=2
	results=a.trial_num(num,strategy, acc_prec_dist)
	a.print_results(results)



if __name__=="__main__":
	main()
