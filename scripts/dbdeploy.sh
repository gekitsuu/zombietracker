# Install 10gen's Key
apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10

echo "deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen" > /etc/apt/sources.list.d/10gen.list

apt-get update
apt-get upgrade -y
apt-get install -y mongodb-10gen python python-setuptools git
easy_install pip
pip install BeautifulSoup

git clone http://github.com/gekitsuu/zombietracker