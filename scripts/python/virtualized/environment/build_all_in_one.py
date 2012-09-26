#!/usr/bin/python
import os
import subprocess
import json
import argparse
import novaaccount
import novaservers

print "Start Build All-In-One"

# Gather the argumetn from the command line
parser = argparse.ArgumentParser()

# Get the role for the server
parser.add_argument('--role', action="store", dest="role", 
					help="Role for the server (Controller / All-In-One / Compute")

# Get the interface for the public network
parser.add_argument('--net_public_iface', action="store", dest="net_public_iface", 
					help="Interface for the public network")

# Get the interface for the private network
parser.add_argument('--net_private_iface', action="store", dest="net_private_iface", 
					help="Interface for the private network")

# Get the IP address of the controller
parser.add_argument('--net_con_ip', action="store", dest="net_con_ip", 
					help="IP address of the controller")

# Get the CIDR block for the Nova Management Network
parser.add_argument('--net_mgmt', action="store", dest="net_mgmt",
					default=" ", help="CIDR block for the Nova Management Network")

# Get the CIDR block for the nova network
parser.add_argument('--net_nova', action="store", dest="net_nova", 
					default="", help="CIDR block for the nova network")

# Get the CIDR block for the public network
parser.add_argument('--net_public', action="store", dest="net_public", 
					default="", help="CIDR block for the public network")

# Get the CIDR block for the Nova Fixed (VM) Network
parser.add_argument('--net_fixed', action="store", dest="net_fixed", 
					help="CIDR block for the Nova Fixed (VM) Network")

# Get the CIDR block for the DMZ Network
parser.add_argument('--net_dmz', action="store", dest="net_dmz", 
					default="", help="CIDR block for the DMZ Network")

# Get the gateway for the DMZ
parser.add_argument('--net_dmz_gateway', action="store", dest="net_dmz_gateway", 
					default="", help="Gateway for the DMZ")

# Get the name of the Nova Fixed Bridge Interface
parser.add_argument('--net_bridge', action="store", dest="net_bridge", 
					default="", help="Name of the Nova Fixed Bridge Interface")

# Get the password for the openstack admin user
parser.add_argument('--os_admin_passwd', action="store", dest="os_admin_passwd", 
					help="Password for the OpenStack admin user")

# Get the username for a normal Openstack user
parser.add_argument('--os_user_name', action="store", dest="os_user_name", 
					help="Username for the normal OpenStack user")

# Get the password for the normal Openstack user
parser.add_argument('--os_user_passwd', action="store", dest="os_user_passwd", 
					help="Password for the normal OpenStack user")

# Save the parameters
results = parser.parse_args()

# Change to the workspace directory, if it doesnt exist, catch the error
workspace_dir = '/var/lib/jenkins/workspace'
try:
	os.chdir(workspace_dir)
	# Run git command to print current commit hash
	subprocess.call(['git', 'log', '-1'])
except OSError:
	print "No Such Directory : %s" % (workspace_dir)

## convert the passed parameters to a json for easy consumption and file writing
server_config = {
	'role' : results.role,
	'net_public_iface' : results.net_public_iface,
	'net_private_iface' : results.net_private_iface,
	'net_con_ip' : results.net_con_ip,
	'net_mgmt' : results.net_mgmt,
	'net_nova' : results.net_nova,
	'net_public' : results.net_public,
	'net_fixed' : results.net_fixed,
	'net_dmz' : results.net_dmz,
	'net_dmz_gateway' : results.net_dmz_gateway,
	'net_bridge' : results.net_bridge,
	'os_admin_passwd' : results.os_admin_passwd,
	'os_user_name' : results.os_user_name,
	'os_user_passwd' : results.os_user_passwd
}
# Print debug
print json.dumps(server_config, indent=2)

## Build a Ubuntu 12.04 Server on our All-In-One box

# Authenticate against our Alamo Install

# These variables will become jenkins variables
url = "http://198.101.133.84:35357"
username = 'admin'
password = 'admin'
tenantid = 'admin'

# Gather Auth info
account_info = novaaccount.generate_account_info(url, username, password, tenantid)
print "Authtoken : " + account_info['authtoken']
print "Account / Tenant : " + account_info['account']
#print json.dumps(account_info, indent=2)

# Gather URL endpoints
urls = novaaccount.urls(account_info['catalogs'])
print json.dumps(urls, indent=2)

# Gather available images
images = novaaccount.images(urls['nova'], account_info['authtoken'])
print json.dumps(images, indent=2)

# Gather available flavors
flavors = novaaccount.flavors(urls['nova'], account_info['authtoken'])
print json.dumps(flavors, indent=2)

# Gather running servers
servers = novaaccount.servers(urls['nova'], account_info['authtoken'])
print json.dumps(servers, indent=2)

"""
new_servers = novaservers.build_servers(account_info['authtoken'], 
									    urls['nova'], 
									    "Alamo Test All-In-One", 
									    1,
									    images['cirros-image'], 
									    "Cirros", 
									    "Alamo Tests", 
									    flavors['m1.tiny']
									   )
## Build the config file to pass to the newly built Ubuntu 12.04 Server
print json.dumps(new_servers, indent=2)
"""

## Tell the Ubuntu Server to run post-install.sh