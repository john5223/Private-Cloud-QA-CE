#!/usr/bin/python

import os
import subprocess
import json
import requests
#from openstack.compute import Compute

workspace_dir = '/var/lib/jenkins/workspace'

## This will become a parameter eventually
num_servers = 3

## Change to the workspace directory, if it doesnt exist, catch the error
try:
	os.chdir(workspace_dir)
except OSError:
	print "No Such Directory : %s" % (workspace_dir)
## Run git command to print current commit hash
subprocess.call(['git', 'log', '-1'])

## Auth against the public cloud api for Rackspace Private Cloud account
print "!!## -- Start Virtualized Setup and Config -- ##!!"
payload = {"auth":{ "RAX-KSKEY:apiKeyCredentials":{ "username":"privateclouddevs", "apiKey":"0e688a460988337e0e759524a2ccfc33"} } }
headers = {'content-type': 'application/json'}
r = requests.post('https://auth.api.rackspacecloud.com/v2.0/tokens', data=json.dumps(payload), headers=headers)

##print json.dumps(r.json, sort_keys=True, indent=2)

account = r.json['access']['token']['tenant']['id']
auth_token = r.json['access']['token']['id']
print "auth_token : %s, account # : %s" % (auth_token, account)

## Step through the JSON and get the Cloud Server endpoints
catalogs = r.json['access']['serviceCatalog']
for catalog in catalogs:
	for endpoint in catalog['endpoints']:
		if('servers' in endpoint.get('publicURL')) and ('2' in endpoint.get('versionId')):
			if('dfw' in endpoint.get('publicURL')):
				## Save the dfw endpint if it exists
				dfw_url = endpoint.get('publicURL')
			elif('ord' in endpoint.get('publicURL')):
				## Save the ord endpoint if it exists
				ord_url = endpoint.get('publicURL')
			else:
				## do nothing with the others
				other_urls += endpoint.get('publicURL')

dfw_headers = {'X-Auth-Token': auth_token, 'content-type': 'application/json'}

## Gather list of images
r = requests.get(dfw_url + '/images/detail', headers=dfw_headers)

## Create a parsable dict with image name and ID that arent snapshots
images = {}
for image in r.json['images']:
	meta_data = image.get('metadata')
	if(meta_data.get('image_type') != 'snapshot'):
		images[image.get('name')] = image.get('id')

# Print the new  images dict in readable form
print json.dumps(images, sort_keys=True, indent=2)

## Gather a list of flavors
r = requests.get(dfw_url + '/flavors', headers=dfw_headers)
flavors = {}
for flavor in r.json['flavors']:
	name = flavor.get('name')
	flavors[name.split(' ')[0]] = flavor.get('id')

# Print the new flavors dict in human readable form
print json.dumps(flavors, sort_keys=True, indent=2)

## We might want to split up the setup from the config into two to three different scripts with classes
## to handle some of the ssh-ing and config file handlings

## In here we will need to spin up servers in our cloud to handle the test build we want to test

## Spin up the passed number of parameters vms
new_build = {"server": {"name" : "Jacob Test Server", "imageRef" : images["Ubuntu 12.04 LTS (Precise Pangolin)"], "flavorRef" : flavors["1GB"], "metadata" : {"My Server Name" : "Ubuntu 12.04 Server"} } }

print json.dumps(new_build, indent=2)

new_build_data = new_build
new_build_headers = {'X-Auth-Token': auth_token, 'content-type': 'application/json', 'X-Auth-Project-Id' : 'test-project'}
r = requests.post(dfw_url + '/servers', data=json.dumps(new_build_data), headers=new_build_headers)

print json.dumps(r.json, sort_keys=True, indent=2)
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