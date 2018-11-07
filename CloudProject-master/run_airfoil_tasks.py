from worker_airfoil_task import airfoilCalc
from flask import Flask
import time
import subprocess
import os
import re
import swiftclient
from celery import Celery, group, subtask

app = Flask(__name__)
@app.route('/')
def  getAngles(angle_start=0, angle_stop=90, angles=45,n_nodes=5,n_levels=0):

	dicti = {}
	listOfResults = []
	pathToMsh = '/home/ubuntu/CloudProject/msh_files/'
	pathToXml = '/home/ubuntu/CloudProject/xml_files/'
	     #Creates .msh with the given parameters.
	meshfiles = subprocess.call(['/home/ubuntu/CloudProject/cloudnaca/./runme.sh', str(angle_start), str(angle_stop), str(angles), str(n_nodes), str(n_levels)])

	     #Converts all .msh files to .xml
        for fil in os.listdir(pathToMsh):
            print(fil)
	     	refinement = re.search('/r(.+?)a', pathToMsh+os.path.splitext(fil)[0]+'.xml')
			if refinement:
				refinement = refinement.group(1)
				if(int(refinement) == int(n_levels)):
					subprocess.call(['dolfin-convert',pathToMsh+fil, pathToXml+os.path.splitext(fil)[0] + '.xml'])
	tasks = [airfoilCalc.s(data['name']) for data in os.listdir(pathToXml)]
	task_group = group(tasks)
	group_res = task_group()
	while(group_res.ready() != True):
	     time.sleep(3)
	if group_res.ready() == True:
    	     result = group_res.get()


	return str(result)

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
