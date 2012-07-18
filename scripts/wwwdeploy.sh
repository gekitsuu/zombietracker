# Install Necessary Packages
dpkg --configure -a
apt-get update
apt-get -y install apache2 wget git python python-setuptools libapache2-mod-wsgi python-software-properties
# apt-get upgrade -y

# Install Python Package
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
su - zombietracker -c 'cd /home/zombietracker; source /home/zombietracker/.virtualenvs/zombietracker/bin/activate; pip install ./zombietracker'

# Restart Apache
service apache2 restart

# Install Saltstack
apt-get install -y python-software-properties
add-apt-repository -y ppa:saltstack/salt
apt-get update
apt-get install -y salt-minion


# sed -i -e "s!#master: salt!master: $MASTERIP!" /etc/salt/minion
