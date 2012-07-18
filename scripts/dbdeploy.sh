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

sudo apt-get install -y python-software-properties
sudo add-apt-repository ppa:saltstack/salt
sudo apt-get update
sudo apt-get install -y salt-master
sudo apt-get install -y salt-minion