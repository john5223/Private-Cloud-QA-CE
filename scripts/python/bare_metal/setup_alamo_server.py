#!/usr/bin/python
"""
	This script connects to our blank ubuntu server and dl's and runs the set-up bash.
"""
import os
import subprocess
import argparse
from ssh_session import ssh_session

print "!!## -- Running Setup for Bare Metal -- ##!!"

# Gather the arguments from the command line
parser = argparse.ArgumentParser()

# Get the hostname for the alamo server
parser.add_argument('-host_name', action="store", dest="host_name", 
					required=True, help="Hostname/IP for the Server")

# Get the username for the host
parser.add_argument('-user_name', action="store", dest="user_name", 
					required=True, help="Non-root user name for the host")

# Get the password for the host
parser.add_argument('-user_passwd', action="store", dest="user_passwd", 
					required=True, help="Non-root password for the host")

# Get the url of the file server to pull files from
parser.add_argument('-file_server_url', action="store", dest="file_server_url",
					default="http://198.31.203.76/alamo/prepare-alamo-server.sh", help="The location to get the prepare script")

# Get the password for the host
parser.add_argument('-v', action="store", dest="verbose", 
					default=None, help="Verbose")

# Parse the parameters
results = parser.parse_args()

# Change to the workspace directory, if it doesnt exist, catch the error
workspace_dir = '/var/lib/jenkins/workspace'
try:
	os.chdir(workspace_dir)
	# Run git command to print current commit hash
	subprocess.call(['git', 'log', '-1'])
except OSError:
	print "No Such Directory : %s" % (workspace_dir)

# Connect to the host
session = ssh_session(results.user_name, results.host_name, results.user_passwd, results.verbose)

# Download the set-up script
session.ssh('wget %s' % (results.file_server_url))

# Run the script that we just downloaded
session.ssh('chmod prepare-alamo-server.sh')
session.ssh('./prepare-alamo-server.sh')

print "!!## -- Ending Setup for Bare Metal -- ##!!"