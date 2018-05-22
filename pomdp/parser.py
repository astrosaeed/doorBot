#!/usr/bin/env python
import os
import sys
import subprocess

class Solver:
	def __init__(self):
		path = '/home/saeid/software/sarsop/src/pomdpsol'
		if os.path.exists(path):
			subprocess.check_output(path + ' program.pomdp --timeout 5 --output program.policy', shell=True)
			#subprocess.call(path + ' program.pomdp --timeout 5 --output program.policy', shell=True)




def main():

	Solver()



if __name__=="__main__":
	main()