#!/usr/bin/python

import argparse

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