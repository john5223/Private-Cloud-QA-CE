#!/usr/bin/python
import os
import subprocess
import json
import argparse
import novaaccount
import novaservers

# Gather the arguments from the command line
parser = argparse.ArgumentParser()

# Get the role for the server
parser.add_argument('--url', action="store", dest="url", 
					help="URL of the Alamo AIO Cluster")

# Get the interface for the public network
parser.add_argument('--username', action="store", dest="username", 
					help="Username of the user building the server")

# Get the interface for the private network
parser.add_argument('--password', action="store", dest="password", 
					help="Password of the user building the server")

# Get the IP address of the controller
parser.add_argument('--tenant_id', action="store", dest="tenant_id", 
					help="Tenant name of the user building the server")

# Get the number of servers to create
parser.add_argument('--num_servers', action="store", dest="num_servers", 
					help="Number of servers to create.")

# Get the name of the server
parser.add_argument('--server_name', action="store", dest="server_name", 
					help="Name of server.")

# Get the OS image to use on the server
parser.add_argument('--os_image', action="store", dest="os_image", 
					help="Operating system to install.")

# Get the flavor that the server will use
parser.add_argument('--server_flavor', action="store", dest="server_flavor", 
					help="Flavor of Server to use ( in MB, GB, etc.).")

# Parse the parameters
results = parser.parse_args()

print results

## Build a Ubuntu 12.04 Server on our All-In-One box
# Authenticate against our Alamo Install

# Gather Auth info
account_info = novaaccount.generate_account_info(results.url, results.username, results.password, results.tenant_id)
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

new_servers = novaservers.build_servers(account_info['authtoken'],
									  urls['nova'],
									  results.server_name,
									  results.num_servers,
									  images[results.os_image],
									  results.os_image,
									  results.tenant_id,
									  flavors[results.server_flavor])

# print debugging
print json.dumps(new_servers, indent=2)