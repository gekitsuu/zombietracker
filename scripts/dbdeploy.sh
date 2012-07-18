# Install MongoDB
apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
echo "deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen" > /etc/apt/sources.list.d/10gen.list

# Update the system
apt-get update
apt-get upgrade -y
apt-get install -y mongodb-10gen python python-setuptools git swig libssl-dev python-dev
easy_install pip
pip install BeautifulSoup pymongo

# Pull Down Zombie Tracker
git clone http://github.com/gekitsuu/zombietracker

# Lockdown Mongo
mongo /root/zombietracker/scripts/lockdown.js
sed -i -e "s!#auth =True!auth = True!" /etc/mongodb.conf
service mongodb restart

# Populate The Database

DBIP=`ifconfig eth0|grep 'inet addr'|awk -F':' '{print $2}'|awk '{print $1}'`
USERNAME=EliteZombieTracker
PASSWORD=impossiblepassword

sed -i -e "s!%IP%!$USERNAME:$PASSWORD@$DBIP!" /root/zombietracker/configs/dbcreds.json
cd /root/zombietracker/
pip install ./
python scripts/scraper.py

# Install Salt
cd /root/
wget https://github.com/downloads/saltstack/salt/salt_0.9.5.pre-v0.9.4-10-g8182e48-1_all.deb
dpkg -i salt_0.9.5.pre-v0.9.4-10-g8182e48-1_all.deb