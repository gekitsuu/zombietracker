# Update teh system
apt-get update
apt-get upgrade -y

# Install Necessary Packages
apt-get -y install apache2 wget git python python-setuptools libapache2-mod-wsgi 

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

# Install Salt
cd /root/
wget https://github.com/downloads/saltstack/salt/salt_0.9.5.pre-v0.9.4-10-g8182e48-1_all.deb
dpkg -i salt_0.9.5.pre-v0.9.4-10-g8182e48-1_all.deb