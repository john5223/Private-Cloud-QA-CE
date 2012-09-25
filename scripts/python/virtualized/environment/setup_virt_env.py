#!/usr/bin/python
import os
import json
import argparse
import subprocess
import cloudaccount

"""
	This script will setup each one of the servers to run
	chef against our chef server as a client
"""

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

	#print "account_info : %s" % json.dumps(account_info, indent=2)

	#close the file
	fo.close()

	# print message for debugging
	print "%s-server-info.json successfully read into account_info" % (results.username)

print server_info