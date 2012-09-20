import json
import requests

def buildservers(authtoken, url, name, numservers, osimageref, osimagename, projectname, flavor):
	"""
		Creates numservers amount of servers and returns the list of created servers
	"""
	print ("authtoken: %s, url : %s, name : %s, numservers : %s, osimageref : %s, osimagename %s, projectname : %s, flavor : %s" 
		   % (authtoken, url, name, numservers, osimageref, osimagename, projectname, flavor))

	new_servers = []
	for i in range(int(numservers)):
		new_server = buildserver(authtoken, url, name + ' ' + str(i), osimageref, osimagename, projectname, flavor)
		new_servers.append(new_server)

	return new_servers

def buildserver(authtoken, url, name, osimageref, osimagename,  projectname, flavor):
	"""
		Builds a new server on the account using the api for the give url
	"""
	# print for debugging
	print ("name : %s, url : %s, osimageref : %s, osimagename: %s, project : %s, flavor : %s" 
		   % (name, url, osimageref, osimagename, projectname, flavor))

	# build json to submit
	new_build = {
				"server": 
					{
						"name" : name, 
						"imageRef" : osimageref, 
						"flavorRef" : flavor, 
						"metadata" : 
							{
								"My Server Name" : osimagename
							} 
					}
				}

	# print for debugging
	print json.dumps(new_build, indent=2)

	# submit call to public cloud api to build server
	new_build_data = new_build
	new_build_headers = {'X-Auth-Token': authtoken, 'content-type': 'application/json', 'X-Auth-Project-Id' : projectname}
	r = requests.post(url + '/servers', data=json.dumps(new_build_data), headers=new_build_headers)

	#print return for debugging
	print json.dumps(r.json, sort_keys=True, indent=2)

	return r.json
