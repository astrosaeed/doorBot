import subprocess	
import random

class Reason:
	def __init__(self):
		pass		
		

	def query(self,filename,intention,time,location,observation):
		#appending the query line at the end of the plog file
		f = open(filename, 'a+')
		f.write("\n?{intention("+time+","+location+")="+intention+"}| obs("+observation+") .")
		f.close()
		temp = subprocess.check_output('plog -t '+filename, shell=True)
		lines = temp.splitlines()
		prob = lines[3].split()[2]
		print "\n{intention("+time+","+location+")="+intention+"| obs("+observation+")}=" ,prob
		return prob
	def delete(self,filename):

		#deleting the query line for future use
		readFile = open(filename)
		lines = readFile.readlines()
		readFile.close()
		w = open(filename,'w')
		w.writelines([item for item in lines[:-1]])
		w.close()

def main():
	a = Reason()
	time = ['rush', 'break']
	location = ['at_entrance','at_exit']
	decision = ['interested', 'not_interested']
	obs  = ['currenttime=','atlocation=']
	

	for i in range(30):
		obs_rand =random.choice(obs)
		time_rand = random.choice(time)
		loc_rand = random.choice(location)
		if obs_rand =='currenttime=': 
			a.query('reason.plog',random.choice(decision), time_rand,random.choice(location),'currenttime=' + time_rand)
		elif obs_rand =='atlocation=':
			a.query('reason.plog',random.choice(decision),time_rand,loc_rand,'atlocation='+ loc_rand)
		a.delete('reason.plog')	

	#a.query('reason.plog','interested','rush','at_entrance','currenttime=rush')
	#a.delete('reason.plog')



if __name__=="__main__":
	main()
