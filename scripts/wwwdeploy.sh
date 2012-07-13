apt-get update
apt-get upgrade -y
apt-get -y install apache2 wget git python python-setuptools libapache2-mod-wsgi 

easy_install pip
pip install virtualenv virtualenvwrapper

# Create the zombietracker user for our app
useradd -m -s /bin/bash zombietracker
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/zombietracker/.bashrc
su zombietracker -c 'source /usr/local/bin/virtualenvwrapper.sh;mkvirtualenv zombietracker'

cd /home/zombietracker 
git clone http://github.com/gekitsuu/zombietracker

cp /home/zombietracker/zombietracker/configs/apache.conf /etc/apache2/sites-available/default

su zombietracker -c '/home/zombietracker/.virtualenvs/zombietracker/bin/pip install flask pymongo'
su zombietracker -c '/home/zombietracker/.virtualenvs/zombietracker/bin/python /home/zombietracker/zombietracker/setup.py install'

service apache2 restart