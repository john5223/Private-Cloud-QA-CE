import os
import subprocess

# Change to the workspace directory
os.chdir('/var/lib/jenkins/workspace')

# Run git command to print current commit hash
subprocess.call(['git', 'log', '-1'])

# Run Things
print "!!## -- Start Virtualized Setup and Config -- ##!!"

## We might want to split up the setup from the config into two to three different scripts with classes
## to handle some of the ssh-ing and config file handlings

## In here we will need to spin up servers in our cloud to handle the test build we want to test

## We will also need to have a config file that is saved in the repo that we can access and push
## to the cloud server (an ISO for a fresh Ubuntu / Red Hat / RAX install)

## Might want to make the script parameterized to pick which distro we are installing on
## i.e -os UB / RH / RX

## We need to make the name of the server a parameter so we can get the IP from the name
## i.e -name NAME

## Once we are done with the setup and config we need to pull the IP and loop pinging till
## we get a response, i.e 
##		while (ping_response == false && ping_count <= 10): 
##			ping_response = subprocess.call(['ping', '$IP'])
##			ping_count++ 

## Once we get a ping response we will need to log into the box and execute an ping to
## the outside world to make sure resolution is occuring
## ( i.e
##		ping_world = subprocess.call(['ping','www.google.com']).status
##		while(ping_world != 'success'):
##			ping_world = subprocess.call(['ping','www.google.com']).status

## Might want to make the testing parameterized for which parts of open stack we are wanting to test
## i.e -branches NSG (Nova / Swift / Glance)

## Once we reach the outside world we will need to make the script take another parameter which 
## tells it what GitHub HASH of openstack we want to pull from / or if blank, pull the latest trunk

## Install OpenStack and the passed branches from the passed repo
print "!!## -- Finished Virtualized Setup and Config -- ##!!"