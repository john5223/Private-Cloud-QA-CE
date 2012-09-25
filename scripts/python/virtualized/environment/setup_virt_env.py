#!/usr/bin/python
import os
import json
import argparse
import subprocess
import cloudaccount
import cloudservers

"""
	This script will setup each one of the servers to run the Alamo ISO without actually running the ISO.
	It will need to assign a role to each machine, then from that role gather information about the server
	from the server. Once all the needed info is gathered it will run a subscript that will configure the server
	to run the alamo post-install.sh
"""

print "!!##-- Begin setup of cloud server enviroment --##!!"

# Gather the arguments from the command line
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
	fo = open("%s-server-info.json" % (results.username), "r")
except IOError:
	print "Failed to open file %s-server-info.json" % (results.username)
else:
	# Write the json string
	server_info = json.loads(fo.read())

	#close the file
	fo.close()

	# print message for debugging
	print "%s-server-info.json successfully read into account_info" % (results.username)

# Loop through the json determining which server will be the controller and which will be the compute
for server in server_info:
	if '0' in server:
		server_info[server]['role'] = 'All-In-One'
	else:
		server_info[server]['role'] = 'Compute'

print json.dumps(server_info, sort_keys=True, indent=2)


print "!!##-- End setup of cloud server enviroment --##!!"