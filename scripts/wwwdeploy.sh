apt-get update
apt-get upgrade -y
apt-get -y install apache2 wget git python-stuptools libapache2-mod-wsgi 

easy_install pip
pip install flask pymongo virtualenv virtualenvwrapper

su zombietracker -c 'mkvirtualenv zombietracker'

# Create the zombietracker user for our app
useradd zombietracker

cd /opt
git clone http://github.com/gekitsuu/zombietracker
chown -R zombietracker:www-data /opt/zombietracker
