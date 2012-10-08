#!/usr/bin/python

import os
import subprocess
import argparse
from ssh_session import ssh_session

"""
	This script connects to our blank ubuntu server and dl's and runs the set-up bash.
"""

print "!!## -- Start Setup Alamo Server -- ##!!"

# Gather the arguments from the command line
parser = argparse.ArgumentParser()

# Get the hostname for the alamo server
parser.add_argument('--host_name', action="store", dest="host_name", 
					required=True, help="Hostname/IP for the Server")

# Get the username for the host
parser.add_argument('--user_name', action="store", dest="user_name", 
					required=True, help="Non-root user name for the host")

# Get the password for the host
parser.add_argument('--user_passwd', action="store", dest="user_passwd", 
					required=True, help="Non-root password for the host")

# Location of the file on the file system
parser.add_argument('--file_location', action="store", dest="file_location",
					required=True, help="Location of the setup file on system running script")

# File name of file to be transferred
parser.add_argument('--setup_file', action="store", dest="setup_file",
					required=True, help="The location to get the setup file")

# Get the password for the host
parser.add_argument('--v', action="store", dest="verbose", 
					default=True, help="Verbose")

# Parse the parameters
results = parser.parse_args()

# Connect to the host
print "Connecting to %s..." % results.host_name
my_session = ssh_session(results.user_name, results.host_name, results.user_passwd, results.verbose)
print "...Done"

# scp the setup file to the server
print "Copying %s to %s:%s/%s..." % (results.setup_file, results.user_name, results.host_name, '')
my_session.scp('%s/%s' % (results.file_location, results.setup_file), '')
print "...Done"

print "Changing permissions to 0755 on %s@%s..." % (results.setup_file, results.host_name)
my_session.ssh('chmod 0755 %s' % results.setup_file)
print "...Done"

# scp the rpcs.cfg file to the server
print "Copying rpcs.cfg to %s@%s/%s..." %(results.user_name, results.host_name, '')
my_session.scp('%s-rpcs.cfg' % results.host_name, '')
print "...Done"

# scp the functions.sh script to the server
print "Copying functions.sh to the server..."
my_session.scp('scripts/bash/functions.sh', '')
print "...Done"

# scp the post-install.sh script to the server
print "Copying post-install.sh to the server..."
my_session.scp('scripts/bash/post-install.sh', '')
print "...Done"

# Close the SSH Session
print "Closing SSH Session..."
my_session.close()
print "...Done"

print "!!## -- Setup for Bare Metal Finished -- ##!!"