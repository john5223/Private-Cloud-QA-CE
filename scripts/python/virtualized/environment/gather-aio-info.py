#!/user/bin/python
"""
--role $ROLE --net_public_iface $NET_PUBLIC_IFACE --net_private_iface $NET_PRIVATE_IFACE --net_con_ip $NET_CON_IP --net_mgmt $NET_MGMT --net_nova $NET_NOVA --net_public $NET_PUBLIC --net_fixed $NET_FIXED --net_dmz $NET_DMZ --net_dmz_gateway $NET_DMZ_GATEWAY --net_bridge $NET_BRIDGE --os_admin_passwd $OS_ADMIN_PASSWD --os_user_name $OS_USER_NAME --os_user_passwd $OS_USER_PASSWD
"""

print "Start Build All-In-One"

# Gather the argumetn from the command line
parser = argparse.ArgumentParser()

# Get the role for the server
parser.add_argument('--role', action="store", dest="role", 
					help="Role for the server (Controller / All-In-One / Compute")

# Get the interface for the public network
parser.add_argument('--net_public_iface', action="store", dest="net_public_iface", 
					help="Interface for the public network")

# Get the interface for the private network
parser.add_argument('--net_private_iface', action="store", dest="net_private_iface", 
					help="Interface for the private network")

# Get the IP address of the controller
parser.add_argument('--net_con_ip', action="store", dest="net_con_ip", 
					help="IP address of the controller")

# Get the CIDR block for the Nova Management Network
parser.add_argument('--net_mgmt', action="store", dest="net_mgmt",
					default=" ", help="CIDR block for the Nova Management Network")

# Get the CIDR block for the nova network
parser.add_argument('--net_nova', action="store", dest="net_nova", 
					default="", help="CIDR block for the nova network")

# Get the CIDR block for the public network
parser.add_argument('--net_public', action="store", dest="net_public", 
					default="", help="CIDR block for the public network")

# Get the CIDR block for the Nova Fixed (VM) Network
parser.add_argument('--net_fixed', action="store", dest="net_fixed", 
					help="CIDR block for the Nova Fixed (VM) Network")

# Get the CIDR block for the DMZ Network
parser.add_argument('--net_dmz', action="store", dest="net_dmz", 
					default="", help="CIDR block for the DMZ Network")

# Get the gateway for the DMZ
parser.add_argument('--net_dmz_gateway', action="store", dest="net_dmz_gateway", 
					default="", help="Gateway for the DMZ")

# Get the name of the Nova Fixed Bridge Interface
parser.add_argument('--net_bridge', action="store", dest="net_bridge", 
					default="", help="Name of the Nova Fixed Bridge Interface")

# Get the password for the openstack admin user
parser.add_argument('--os_admin_passwd', action="store", dest="os_admin_passwd", 
					help="Password for the OpenStack admin user")

# Get the username for a normal Openstack user
parser.add_argument('--os_user_name', action="store", dest="os_user_name", 
					help="Username for the normal OpenStack user")

# Get the password for the normal Openstack user
parser.add_argument('--os_user_passwd', action="store", dest="os_user_passwd", 
					help="Password for the normal OpenStack user")

# Save the parameters
results = parser.parse_args()

# Change to the workspace directory, if it doesnt exist, catch the error
workspace_dir = '/var/lib/jenkins/workspace'
try:
	os.chdir(workspace_dir)
	# Run git command to print current commit hash
	subprocess.call(['git', 'log', '-1'])
except OSError:
	print "No Such Directory : %s" % (workspace_dir)

## convert the passed parameters to a json for easy consumption and file writing
server_config = {
	'role' : results.role,
	'net_public_iface' : results.net_public_iface,
	'net_private_iface' : results.net_private_iface,
	'net_con_ip' : results.net_con_ip,
	'net_mgmt' : results.net_mgmt,
	'net_nova' : results.net_nova,
	'net_public' : results.net_public,
	'net_fixed' : results.net_fixed,
	'net_dmz' : results.net_dmz,
	'net_dmz_gateway' : results.net_dmz_gateway,
	'net_bridge' : results.net_bridge,
	'os_admin_passwd' : results.os_admin_passwd,
	'os_user_name' : results.os_user_name,
	'os_user_passwd' : results.os_user_passwd
}
# Print debug
print json.dumps(server_config, indent=2)