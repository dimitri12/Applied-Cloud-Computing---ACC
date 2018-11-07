#!/usr/bin/python
import sys
import subprocess
import os
import time


subprocess.call('~/CloudProject/InitMaster.sh', shell=True)


with open('/home/ubuntu/CloudProject/floating_ip.txt', 'r') as float_ip:
	floating_ip = float_ip.readline()
with open('/home/ubuntu/CloudProject/WorkerCloud_config.txt', 'r') as file:
	data = file.readlines()
data[15] = ' - echo ' + floating_ip + ' > floating_ip.txt\n'
with open('/home/ubuntu/CloudProject/WorkerCloud_config.txt', 'w') as file:
	file.writelines( data )

n_workers = 4
for i in range(n_workers):
	with open('/home/ubuntu/CloudProject/WorkerCloud_config.txt', 'r') as file:
		data = file.readlines()
		data[18] = ' - celery -A worker_airfoil_task worker --loglevel=info --autoscale=1,1 -n worker'+str(i)+'\n'
	with open('/home/ubuntu/CloudProject/WorkerCloud_config.txt', 'w') as file:
		file.writelines( data )
	os.system('python /home/ubuntu/CloudProject/InitScript.py create Worker'+ str(i))
print('Sleeping for 60 seconds')
time.sleep(60)
