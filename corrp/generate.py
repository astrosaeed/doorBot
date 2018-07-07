import subprocess
pomdpsol = '/home/saeid/software/sarsop/src/pomdpsol'

filename='program.pomdp'
policyfile='program.policy'
subprocess.check_output([pomdpsol, filename, \
    '--timeout', '160', '--output', policyfile])
print 'Finished training'