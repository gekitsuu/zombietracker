apt-get update
apt-get upgrade -y
apt-get -y install apache2 wget git python python-setuptools libapache2-mod-wsgi 

easy_install pip
pip install flask pymongo virtualenv virtualenvwrapper

# Create the zombietracker user for our app
useradd -m -s /bin/bash zombietracker
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/zombietracker/.bashrc
su zombietracker -c 'mkvirtualenv zombietracker'

cd /opt
git clone http://github.com/gekitsuu/zombietracker
chown -R zombietracker:www-data /opt/zombietracker

