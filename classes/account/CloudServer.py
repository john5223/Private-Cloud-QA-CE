import requests
import json
from account import Account

class CloudServer():
	""" Base class for a cloud server account"""
	
	def __init__(self, account):
		""" Initializes and builds the Cloud Server Account"""
		self.account = account
		self.cloud_server_json()
		self.gen_auth_token()
		self.catalogs()
		self.gen_server_urls()
		self.images()
		self.flavors()

	## generates a auth token for the account
	def cloud_server_json(self):
		""" This method connects to Rackspace Public Cloud APIU and returns a JSON of the requested cloud server"""
		
		# data to be sent to the cloud servers auth
		payload = {"auth":
			{"RAX-KSKEY:apiKeyCredentials":
				{"username":self.account.username, "apiKey":self.account.apikey} 
			} 
		}

		# headers to send to the cloud servers auth
		headers = {'content-type': 'application/json'}

		# send auth request
		r = requests.post('https://auth.api.rackspacecloud.com/v2.0/tokens', data=json.dumps(payload), headers=headers)

		## return the generated json
		self.csjson = r.json

	## Gather the auth token
	def auth_token(self):
		""" Gets the auth token for connecting to the cloud server api"""
		self.auth_token = self.json['access']['token']['id']

	## Gather the account number
	def account_number(self):
		""" Gets the account number for the Cloud Server Account"""
		self.account_num = self.json['access']['token']['tenant']['id']

	## generates the catalog dict for the cloud server account
	def catalogs(self):
		""" Gets the catalog that is returned from the Rackspace Public Cloud request"""
		self.catalogs = self.csjson['access']['serviceCatalog']

	## creates the images for the cloud server account
	def images(self):
		""" Gets the images from the JSON that was returned"""
		# create the auth headers to talk to dfw cloud servers for account
		headers = {'X-Auth-Token': self.auth_token, 'content-type': 'application/json'}

		# Gather list of images
		r = requests.get(self.dfw_url + '/images/detail', headers=headers)

		# Create a parsable dict with image name and ID that arent snapshots
		images = {}
		for image in r.json['images']:
			meta_data = image.get('metadata')
			if(meta_data.get('image_type') != 'snapshot'):
				images[image.get('name')] = image.get('id')

		# print json.dumps(images, sort_keys=True, indent=2)
		self.images = images

	## populates the cloud server
	def flavors(self):
		""" Gets the flavors from the JSON that was returned by Rackspace Public Cloud"""
		## Gather a list of flavors
		r = requests.get(dfw_url + '/flavors', headers=dfw_headers)
		
		flavors = {}
		for flavor in r.json['flavors']:
			name = flavor.get('name')
			flavors[name.split(' ')[0]] = flavor.get('id')

		# Print the new flavors dict in human readable form
		# print json.dumps(flavors, sort_keys=True, indent=2)
		self.flavors = flavors

	def gen_server_urls(self):
		""" Gets the server urls for talking to the API for the account"""
		for catalog in self.catalogs:
			for endpoint in catalog['endpoints']:
				if('servers' in endpoint.get('publicURL')) and ('2' in endpoint.get('versionId')):
					if('dfw' in endpoint.get('publicURL')):
						## Save the dfw endpint if it exists
						self.dfw_url = endpoint.get('publicURL')
					elif('ord' in endpoint.get('publicURL')):
						## Save the ord endpoint if it exists
						self.ord_url = endpoint.get('publicURL')
					else:
						## do nothing with the others
						self.other_urls += endpoint.get('publicURL')
