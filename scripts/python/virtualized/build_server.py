#!/usr/bin/python
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--number', action="store", dest="num_servers", 
					default="1", help="Number of servers to create. Default : 1")
parser.add_argument('--name', action="store", dest="server_name", 
					default="Alamo Virtualization Test", help="Name of server. Default : Alamo Virtualization Test")
parser.add_argument('--project', action="store", dest="project_name", 
					default="Alamo Virtualization Tests", help="Name of project that servers will belong to. Default : Alamo Virtualization Tests")
parser.add_argument('--os', action="store", dest="os_image", 
					default="Ubuntu 12.04", help="Operating system to install. Default: Ubuntu 12.04")
parser.add_argument('--flavor', action="store", dest="server_flavor", 
					default="1GB", help="Flavor of Server to use. Default : 1GB")

results=parser.parse_args()

new_build = {
				"server": 
				{
					"name" : results.server_name, 
					"imageRef" : "5cebb13a-f783-4f8c-8058-c4182c724ccd", 
					"flavorRef" : "3", 
					"metadata" : 
						{
							"My Server Name" : "Ubuntu 12.04 Server"
						} 
				}
			}

print json.dumps(new_build, indent=2)


# submit call to public cloud api to build server
#new_build_data = new_build
#new_build_headers = {'X-Auth-Token': auth_token, 'content-type': 'application/json', 'X-Auth-Project-Id' : 'test-project'}
#r = requests.post(dfw_url + '/servers', data=json.dumps(new_build_data), headers=new_build_headers)
#print json.dumps(r.json, sort_keys=True, indent=2)