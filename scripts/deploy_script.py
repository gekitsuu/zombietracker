from gevent import monkey
from libcloud.compute.deployment import MultiStepDeployment
from libcloud.compute.deployment import ScriptDeployment
from libcloud.compute.deployment import SSHKeyDeployment

import gevent
import json
import libcloud.security
import libcloud.compute.providers
import libcloud.compute.types
import libcloud.loadbalancer.base
import libcloud.loadbalancer.providers
import libcloud.loadbalancer.types
import os.path
import re
import time


# Monkey Patch for gevent
monkey.patch_all()

#  My prefrence is to reference my credentials from a seperate file named
# creds.json. The file format should be like this:
# {
#       "username": "your username",
#       "apikey": "your apikey"
# }

# Read in my config file
config = json.loads(open(os.path.expanduser('~/.rsnovacreds.json')).read())

# Had CA errors on my Mac so I set this option to False, it should be True
libcloud.security.VERIFY_SSL_CERT = False  # This is a bad idea

# Get the driver object
# For UK accounts use Provider.RACKSPACE_NOVA_LON
CompRackspace = libcloud.compute.providers.get_driver(libcloud.compute.types.Provider.RACKSPACE_NOVA_DFW)

# Use the compute driver to create a connection
compdriver = CompRackspace(config['username'], config['apikey'],
    ex_force_auth_url='https://identity.api.rackspacecloud.com/v2.0/',
    ex_force_auth_version='2.0')

images = compdriver.list_images()  # Get a list of images
sizes = compdriver.list_sizes()    # Get a list of server sizes

size = [s for s in sizes if s.ram == 512][0]  # Get the 512MB sized machine
image = [i for i in images if i.name == 'Ubuntu 12.04 LTS (Precise Pangolin)'][0]  # Debian Img

install_key = SSHKeyDeployment(
    open(os.path.expanduser("~/.ssh/id_rsa.pub")).read())
install_apache = ScriptDeployment(
    open(os.path.expanduser("./wwwdeploy.sh")).read())
install_mongo = ScriptDeployment(
    open(os.path.expanduser("./dbdeploy.sh")))


db_deploy_steps = MultiStepDeployment([install_key, install_mongo])


def mycreatenode(servername, image, size, deploy):
    print("Creating %s with %s and size %s" % (
        servername, image.name, size.name))
    t_CompRackspace = libcloud.compute.providers.get_driver(
        libcloud.compute.providers.Provider.RACKSPACE_NOVA_DFW)

    t_compdriver = t_CompRackspace(config['username'], config['apikey'],
        ex_force_auth_url='https://identity.api.rackspacecloud.com/v2.0/',
        ex_force_auth_version='2.0')

    t_compdriver.deploy_node(
        name=servername, image=image, size=size, deploy=deploy)
    print("Finished creating %s with %s and size %s" %
        (servername, image.name, size.name))

dbsize = [s for s in sizes if s.ram == 2048][0]
mycreatenode('db-zt01.gekitsuu.org', image, dbsize, db_deploy_steps)

dbserver = [x for x in compdriver.list_nodes() if re.match('db.*', x.name)][0]
dbserverip = dbserver.private_ips[0]

# Create 2 512MB Debian Nodes named zombietracker0X.gekitsuu.org
saltscript = str('sed -i -e "s!#master: salt!master: %s!" /etc/salt/minion' % dbserverip)
configure_salt = ScriptDeployment(saltscript)
restart_salt = ScriptDeployment(str('service salt-minion restart'))
restart_apache = ScriptDeployment(str('service apache2 restart'))
configure_db_creds = ScriptDeployment(str('sed -i -e "s!REPLACEME!EliteZombieTracker:impossiblepassword@%s!" /home/zombietracker/zombietracker/configs/dbcreds.json' % dbserverip))
www_deploy_steps = MultiStepDeployment([install_key, install_apache, configure_salt, restart_salt, configure_db_creds, restart_apache])
jobs = []
newservers = ['www-zt01.gekitsuu.org', 'www-zt02.gekitsuu.org']
for servername in newservers:
    jobs.append(gevent.spawn(mycreatenode, servername, image, size, www_deploy_steps))

gevent.joinall(jobs, timeout=600)


www_deploy_steps = MultiStepDeployment([install_key, install_apache])
public_ips = []
keep_going = False
while not keep_going:
    nodes = compdriver.list_nodes()  # Get the list of nodes
    xnodes = [x for x in nodes if re.search('www-zt', x.name)]  # Filter
    node_states = [x.state for x in xnodes]  # Get a list of states

    # Wait for the nodes to be ready (They should be already)
    if libcloud.compute.types.NodeState.PENDING in node_states:
        print("Nodes currently not running")
        time.sleep(10)
    else:
        # Once the nodes are ready continue
        print("Nodes is now running")

        # Get the public IPV4 addresses of the nodes
        for node in xnodes:
            node_ips = node.public_ips
            for ip in node_ips:
                if re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', ip):
                    public_ips.append(ip)
        keep_going = True


# Create a load balancer now that the servers are built
LBRackspace = libcloud.loadbalancer.providers.get_driver(
    libcloud.loadbalancer.types.Provider.RACKSPACE_US)
lbdriver = LBRackspace(config['username'], config['apikey'])

# Create the load balanacer and add the servers
members = [libcloud.loadbalancer.base.Member(None, i, 80) for i in public_ips]
new_balancer = lbdriver.create_balancer(name='zombietracker-lb',
    algorithm=libcloud.loadbalancer.base.Algorithm.ROUND_ROBIN,
    port=80, protocol='http', members=members)
