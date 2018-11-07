import time
import subprocess
import os
import re
import sys
import swiftclient
from celery import Celery

with open('floating_ip.txt', 'r') as float_ip:
	floating_ip = float_ip.readline()
app = Celery('tasks',backend='amqp://',broker='amqp://none:none@'+floating_ip+'/nonevhost')

#Reads the values in drag_ligit.m which has three columns: time, lift, drag. Calculates the mean values of the columns lift and drag and returns them in a dict.
def convert(file_name,angle):
     convertedList = list()
     Lift = 0
     Drag = 0
     i = 0
     with open('/home/ubuntu/CloudProject/results/'+file_name+'results.m') as input_file:
          for _ in xrange(30):
	       next(input_file)
	  for line in input_file:
               a = line.split()
               Lift +=float(a[1])
               Drag +=float(a[2])
               i += 1
     Lift = Lift/i
     Drag = Drag/i
     return {'Angle': angle, 'Lift': Lift, 'Drag': Drag}


@app.task
def airfoilCalc(file_name, samples=10, viscosity=0.0001, speed=10.,airtime=1):

	        dicti = {}
		listOfResults = []
		pathToXmls = '/home/ubuntu/CloudProject/xml_files/'

		os.system('sudo chmod 755 -R /home/ubuntu/CloudProject/xml_files/')

               	print "Doing airfoil on: " + file_name
		time.sleep(2)
		os.system('sudo chmod 755 -R /home/ubuntu/CloudProject/results/')
                subprocess.call(['sudo', '/home/ubuntu/CloudProject/navier_stokes_solver/./airfoil', str(samples), str(viscosity), str(speed), str(airtime), pathToXmls+file_name])
		os.system('sudo chmod 755 -R /home/ubuntu/navier_stokes_solver/results/')
         	os.system('sudo mv /home/ubuntu/navier_stokes_solver/results/drag_ligt.m /home/ubuntu/CloudProject/results/'+file_name+'results.m')
		angle = re.search('a(.+?)n', file_name)
		if angle:
		     angle = angle.group(1)
	             dicti = convert(file_name,int(angle))

                return str(dicti)
