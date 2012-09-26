import json
import requests

def build_servers(authtoken, url, name, numservers, osimageref, osimagename, projectname, flavor):
	"""
		Creates numservers amount of servers and returns the list of created servers
	"""
	print ("authtoken: %s, url : %s, name : %s, numservers : %s, osimageref : %s, osimagename %s, projectname : %s, flavor : %s" 
		   % (authtoken, url, name, numservers, osimageref, osimagename, projectname, flavor))

	servers = []
	for i in range(int(numservers)):
		server = build_server(authtoken, url, name + ' ' + str(i), osimageref, osimagename, projectname, flavor)
		servers.append(server)

	return servers

def build_server(authtoken, url, name, osimageref, osimagename,  projectname, flavor):
	"""
		Builds a new server on the account using the api for the give url
	"""
	# print for debugging
	#print ("name : %s, url : %s, osimageref : %s, osimagename: %s, project : %s, flavor : %s" 
	#	   % (name, url, osimageref, osimagename, projectname, flavor))

	# build json to submit
	build = {
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

	# submit call to public cloud api to build server
	data = build
	headers = {'X-Auth-Token': authtoken, 'content-type': 'application/json', 'X-Auth-Project-Id' : projectname}
	r = requests.post(url + '/servers', data=json.dumps(data), headers=headers)

	content = json.loads(r.content)
	return content

def delete_servers(authtoken, url, serverids):
	"""
		Delete a list of servers by ids
	"""

	success = []
	failed = []
	for serverid in serverids:
		status_code = delete_server(authtoken, url, serverid)
		if status_code == 204:
			success.append(serverid)
		else:
			failed.append(serverid)

	return {'success' : success, 'failed' : failed}

def delete_server(authtoken, url, serverid):
	"""
		Deletes a given server with id
	"""

	print url + '/servers/%s' % serverid
	headers = {'X-Auth-Token': authtoken, 'content-type': 'application/json'}
	r = requests.delete(url + '/servers/%s' % serverid, headers=headers)

	return r.status_code

