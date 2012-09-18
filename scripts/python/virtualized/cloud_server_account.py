#!/usr/bin/python
import json
import requests
import argparse

## parse the command line options for the user and api key
parser = argparse.ArgumentParser()
parser.add_argument('--username', action="store", dest="username", 
					help="User name for the account")
parser.add_argument('--apikey', action="store", dest="apikey", 
					help="api key for the account")
results = parser.parse_args()

## Debug printing
print "username : " + results.username
print "apikey : " + results.apikey

## Auth against the public cloud api for Rackspace Private Cloud account
print "!!## -- Start Cloud Server Account -- ##!!"
## data to be sent to the cloud servers auth
payload = {"auth":
			{"RAX-KSKEY:apiKeyCredentials":
				{"username":results.username, "apiKey":results.apikey} 
			} 
		}
## headers to send to the cloud servers auth
headers = {'content-type': 'application/json'}

## send auth request
r = requests.post('https://auth.api.rackspacecloud.com/v2.0/tokens', data=json.dumps(payload), headers=headers)

## gather account and auth_token and save them for later use
account = r.json['access']['token']['tenant']['id']
auth_token = r.json['access']['token']['id']

## print debugging
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


## create the auth headers to talk to dfw cloud servers for account
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