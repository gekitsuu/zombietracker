# Install 10gen's Key
apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10

echo "deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen" > /etc/apt/sources.list.d/10gen.list

apt-get update
apt-get upgrade -y
apt-get install -y mongodb-10gen python python-setuptools git
easy_install pip
pip install BeautifulSoup pymongo

git clone http://github.com/gekitsuu/zombietracker

mongo /root/zombietracker/scripts/lockdown.js
python /root/zombietracker/scripts/scraper.py

echo "auth = True" >> /etc/mongodb.conf
service mongodb restart

DBIP=`ifconfig eth0|grep 'inet addr'|awk -F':' '{print $2}'|awk '{print $1}'`
USERNAME=EliteZombieTracker
PASSWORD=impossiblepassword

sed -i -e "s!%IP%!$USERNAME:$PASSWORD@$DBIP!" /root/zombietracker/configs/dbcreds.json
