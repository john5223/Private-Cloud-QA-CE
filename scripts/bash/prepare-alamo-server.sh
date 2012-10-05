#!/bin/bash

###################################################################################
## This is a script that is run locally to prepare a server for installing alamo ##
## Author : Solomon Wagner                                                       ##
###################################################################################   

# Image URLS
# Might make the parameters in the future
CIRROS_IMAGE_NAME="cirros-0.3.0-x86_64-uec.tar.gz"
CIRROS_URL="https://launchpadlibrarian.net/83305869/${CIRROS_IMAGE_NAME}"
PRECISE_IMAGE_NAME="precise-server-cloudimg-amd64.tar.gz"
PRECISE_URL="http://cloud-images.ubuntu.com/precise/current/${PRECISE_IMAGE_NAME}"
CHEF_IMAGE_NAME="chef-server.qcow2"
CHEF_IMAGE_HOST=${CHEF_IMAGE_HOST:-c390813.r13.cf1.rackcdn.com}
CHEF_IMAGE_URL="http://${CHEF_IMAGE_HOST}/${CHEF_IMAGE_NAME}"

# Our File Server URLS
FILE_SERVER_URL="http://198.61.203.76/alamo"
POST_INSTALL_LOCATION="post-install.sh"
FUNCTIONS_LOCATION="functions.sh"
RPCS_CFG_LOCATION="${HOSTNAME}-rpcs.cfg"

## CREATE NEEDED DIRECTORIES
# make the /opt/rpcs directory and move into it
echo "Making /opt/rpcs directory"
mkdir -p /opt/rpcs

echo "Moving into /opt/rpcs directory"
cd /opt/rpcs

# Get the hostname of the server
echo "HOSTNAME : ${HOSTNAME}"

# Download the cirros image
if [ `ls | grep $CIRROS_IMAGE_NAME` = $CIRROS_IMAGE_NAME ]; then
	echo "${CIRROS_IMAGE_NAME} already downloaded"
else
	echo "Downloading ${CIRROS_IMAGE_NAME}"
	wget ${CIRROS_URL}
fi

# Download the precise image
if [ `ls | grep $PRECISE_IMAGE_NAME` = $PRECISE_IMAGE_NAME ]; then
	echo "${PRECISE_IMAGE_NAME} already downloaded"
else
	echo "Downloading ${PRECISE_IMAGE_NAME}"
	wget ${PRECISE_URL}
fi

# Download the chef-server image
if [ `ls | grep $CHEF_IMAGE_NAME` = $CHEF_IMAGE_NAME ]; then
	echo "${CHEF_IMAGE_NAME} already downloaded"
else
	echo "Downloading ${CHEF_IMAGE_NAME}"
	wget ${CHEF_IMAGE_URL}
fi

# Download the precise image
if [ `ls | grep $POST_INSTALL_LOCATION` = $POST_INSTALL_LOCATION ]; then
	echo "${POST_INSTALL_LOCATION} already downloaded"
else
	echo "Downloading post-install.sh"
	wget "${FILE_SERVER_URL}/${POST_INSTALL_LOCATION}"
fi

# Download functions.sh
if [ `ls | grep $FUNCTIONS_LOCATION` = $FUNCTIONS_LOCATION ]; then
	echo "${FUNCTIONS_LOCATION} already downloaded"
else
	echo "Downloading functions.sh"
	wget "${FILE_SERVER_URL}/${FUNCTIONS_LOCATION}"
fi

# Download the rpcs.cfg file for this hostname
if [ `ls | grep rpcs.cfg` = 'rpcs.cfg']; then
	echo "rpcs.cfg for this server already downloaded"
else
	# Download the rpcs.cfg for this server		
	echo "Downloading ${HOSTNAME}-rpcs.cfg"
	wget "${FILE_SERVER_URL}/${RPCS_CFG_LOCATION}"

	# Create rpcs.cfg
	echo "Creating rpcs.cfg"
	cp "${HOSTNAME}-rpcs.cfg" rpcs.cfg

	# Delete old rpcs.cfg
	echo "Deleting ${HOSTNAME}-rpcs.cfg"
	rm -r "${HOSTNAME}-rpcs.cfg"
fi

echo "Installing Ubuntu Packages needed to run alamo"
apt-get install -y openssh-server build-essential libvirt-bin qemu-kvm sshpass pwgen dialog curl

echo "Updating packages"
apt-get update
apt-get -y upgrade

# Once we have all we need, run the post-install.sh script
#chmod +x post-install.sh
#./post-install.sh