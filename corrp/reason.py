import subprocess	
import random

class Reason:
	def __init__(self,filename):
		pass		
		self.filename=filename

	def query(self,time,location,lstm):
		#appending the query line at the end of the plog file
		f = open(self.filename, 'a+')
		f.write("\n?{intention=interested}|obs(currenttime="+time+"),obs(atlocation="+location+",obs"+lstm+".")
		f.close()
		temp = subprocess.check_output('plog -t '+self.filename, shell=True)
		lines = temp.splitlines()
		prob = lines[3].split()[2]
		print "\n The probability of {intention=interested|obs"+time+", obs"+location+",obs"+lstm+". =" ,prob
		self.delete()
		return prob


	def query_nolstm(self,time,location):
		#appending the query line at the end of the plog file
		print '\nUsing the distributions provided in P-Log and observations, we query the intention of the person:'
		f = open(self.filename, 'a+')
		f.write("\n?{intention=interested}|obs(currenttime="+time+"),obs(atlocation="+location+").")
		f.close()
		temp = subprocess.check_output('plog -t '+self.filename, shell=True)
		lines = temp.splitlines()
		prob = lines[3].split()[2]
		print "{intention=interested|obs(currenttime="+time+"), obs(atlocation="+location+") = ",prob
		self.delete()
		return prob

	def delete(self):

		#deleting the query line for future use
		readFile = open(self.filename)
		lines = readFile.readlines()
		readFile.close()
		w = open(self.filename,'w')
		w.writelines([item for item in lines[:-1]])
		w.close()

def main():
	a = Reason()
	time = ['(currenttime=morning)', '(currenttime=afternoon)', '(currenttime=evening)']
	location = ['(atlocation=classroom)','(atlocation=library)']
	lstm = ['(classifier=zero)','(classifier=one)']
	decision = ['interested', 'not_interested']
	obs  = ['currenttime=','atlocation=','classifier=']


	

	for i in range(30):
		
		time_rand = random.choice(time)
		loc_rand = random.choice(location)
		lstm_rand = random.choice(lstm)
		
		a.query('reason.plog',random.choice(decision), time_rand,lstm_rand, loc_rand)
		#a.delete('reason.plog')

			

	#a.query('reason.plog','interested','rush','at_entrance','currenttime=rush')
	#a.delete('reason.plog')



if __name__=="__main__":
	main()
