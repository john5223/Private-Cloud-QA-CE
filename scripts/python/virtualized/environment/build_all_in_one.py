#!/usr/bin/python
import os
import subprocess
import json
import argparse

print "Start Build All-In-One"

# Gather the argumetn from the command line
parser = argparse.ArgumentParser()

# Get the role for the server
parser.add_argument('--role', action="store", dest="role", 
					type=str, help="Role for the server (Controller / All-In-One / Compute")

# Get the interface for the public network
parser.add_argument('--net_public_iface', action="store", dest="net_public_iface", 
					type=str, help="Interface for the public network")

# Get the interface for the private network
parser.add_argument('--net_private_iface', action="store", dest="net_private_iface", 
					type=str, help="Interface for the private network")

# Get the IP address of the controller
parser.add_argument('--net_con_ip', action="store", dest="net_con_ip", 
					type=str, help="IP address of the controller")

# Get the CIDR block for the Nova Management Network
parser.add_argument('--net_mgmt', action="store", dest="net_mgmt",
					type=str, default=" ", help="CIDR block for the Nova Management Network")

# Get the CIDR block for the nova network
parser.add_argument('--net_nova', action="store", dest="net_nova", 
					type=str, default="", help="CIDR block for the nova network")

# Get the CIDR block for the public network
parser.add_argument('--net_public', action="store", dest="net_public", 
					type=str, default="", help="CIDR block for the public network")

# Get the CIDR block for the Nova Fixed (VM) Network
parser.add_argument('--net_fixed', action="store", dest="net_fixed", 
					type=str, help="CIDR block for the Nova Fixed (VM) Network")

# Get the CIDR block for the DMZ Network
parser.add_argument('--net_dmz', action="store", dest="net_dmz", 
					type=str, default="", help="CIDR block for the DMZ Network")

# Get the gateway for the DMZ
parser.add_argument('--net_dmz_gateway', action="store", dest="net_dmz_gateway", 
					type=str, default="", help="Gateway for the DMZ")

# Get the name of the Nova Fixed Bridge Interface
parser.add_argument('--net_bridge', action="store", dest="net_bridge", 
					type=str, default="", help="Name of the Nova Fixed Bridge Interface")

# Get the password for the openstack admin user
parser.add_argument('--os_admin_passwd', action="store", dest="os_admin_passwd", 
					type=str, help="Password for the OpenStack admin user")

# Get the username for a normal Openstack user
parser.add_argument('--os_user_name', action="store", dest="os_user_name", 
					type=str, help="Username for the normal OpenStack user")

# Get the password for the normal Openstack user
parser.add_argument('--os_user_passwd', action="store", dest="os_user_passwd", 
					type=str, help="Password for the normal OpenStack user")

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

print results
