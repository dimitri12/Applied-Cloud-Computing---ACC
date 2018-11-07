cd /home/ubuntu/

#sudo pip install Celery
#sudo apt-get install rabbitmq-server -y

git clone https://github.com/marcusfroling/CloudProject.git
sudo mkdir /home/ubuntu/CloudProject/geo_files/
sudo mkdir /home/ubuntu/CloudProject/msh_files/
sudo mkdir /home/ubuntu/CloudProject/results/
sudo mkdir /home/ubuntu/CloudProject/xml_files/

sudo service rabbitmq-server start

sudo rabbitmqctl add_user none none
sudo rabbitmqctl add_vhost nonevhost
sudo rabbitmqctl set_permissions -p nonevhost none ".*" ".*" ".*"

sudo rm -rf /home/ubuntu/murtazo
sudo rm -f /home/ubuntu/murtazo.tgz

cd /home/ubuntu/CloudProject

screen -d -m python run_airfoil_tasks.py