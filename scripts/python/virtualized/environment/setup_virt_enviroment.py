#!/usr/bin/python

import os
import json
import argparse
import subprocess
import cloudaccount

# Gather the argumetn from the command line
parser = argparse.ArgumentParser()

# Get the username for the Rackspace Public Cloud Account
parser.add_argument('--username', action="store", dest="username", 
					help="User name for the account")

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

try:
	# Open the file
	fo = open("%s-build.json" % (results.username), "r")
except IOError:
	print "Failed to open file %s-build.json" % (results.username)
else:
	# Write the json string
	account_info = json.loads(fo.read())

	#print "account_info : %s" % json.dumps(account_info, indent=2)

	#close the file
	fo.close()

	# print message for debugging
	print "%s-build.json successfully read into account_info" % (results.username)

curr_servers = cloudaccount.servers(account_info['urls']['dfw'], account_info['authtoken'])

# Loop through the new servers and the current runnins server to gather needed info to setup
servers = {}
# Find the public and private ips of the new servers
for new_server in account_info['new_servers']:
	for curr_server in curr_servers:
		if new_server['server']['id'] in curr_servers[curr_server]['id']:
			name = curr_server
			admin_user = 'admin'
			admin_pass = new_server['server']['adminPass']
			public_ip = curr_servers[curr_server]['public_ip']
			private_ip = curr_servers[curr_server]['private_ip']
			servers[name] = {'user' : admin_user,
					  		 'admin_pass' : admin_pass,
					  		 'public_ip' : public_ip,
					  		 'private_ip' : private_ip
					  		 }

#print json.dumps(servers, sort_keys=True, indent=2)

# Need to either save these into enviroment variables and use jenkins to ssh into the boxes and set up
# chef, or do it here in the script via a module

# Write build_info as a json file
try:
	# Open the file
	fo = open("%s-setup.json" % (results.username), "w")
except IOError:
	print "Failed to open file %s-setup.json" % (results.username)
else:
	# Write the json string
	fo.write(json.dumps(servers, indent=2))
	#clost the file
	fo.close()
	print "!! %s-setup.json file write successful!!" % (results.username)