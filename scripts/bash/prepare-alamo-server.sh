#!/bin/bash

###################################################################################
## This is a script that is run locally to prepare a server for installing alamo ##
## Author : Solomon Wagner                                                       ##
################################################################################### 

#check to make sure user can be root
if [ `whoami` != "root" ]; then
    echo "Can only run script as root"; exit;
fi

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

echo "Installing Ubuntu Packages needed to run alamo..."
apt-get install -y openssh-server build-essential libvirt-bin qemu-kvm sshpass pwgen dialog curl
echo "...Done"

echo "Updating packages..."
apt-get update
apt-get -y upgrade
echo "...Done"

## CREATE NEEDED DIRECTORIES
# make the /opt/rpcs directory and move into it
echo "Making /opt/rpcs directory..."
mkdir -p /opt/rpcs
echo "...Done"

echo "Moving post-install.sh to /opt/rpcs..."
mv /home/administrator/post-install.sh /opt/rpcs 
echo "...Done"

echo "Moving functions.sh to /opt/rpcs..."
mv /home/administrator/functions.sh /opt/rpcs 
echo "...Done"

echo "Moving post-install.sh to /opt/rpcs..."
mv /home/administrator/post-install.sh /opt/rpcs 
echo "...Done"

#Get ip address for eth0 (hopefully public ip) 
ip=`ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
echo "eth0 ip address: $ip"

echo "Copying $ip-rpcs.cfg to rpcs.cfg..."
cp $ip-rpcs.cfg rpcs.cfg
echo "...Done"

echo "Moving rpcs.cfg into /opt/rpcs directory..."
mv /home/administrator/rpcs.cfg /opt/rpcs
echo "...Done"

echo "Move into /opt/rpcs"
cd /opt/rpcs
pwd
echo "...Done"

# Get the hostname of the server
echo "HOSTNAME : ${HOSTNAME}"

# Download the cirros image
if [ `ls | grep $CIRROS_IMAGE_NAME` = $CIRROS_IMAGE_NAME ]; then
	echo "${CIRROS_IMAGE_NAME} already downloaded"
else
	echo "Downloading ${CIRROS_IMAGE_NAME}..."
	wget ${CIRROS_URL}
	echo "...Done"
fi

# Download the precise image
if [ `ls | grep $PRECISE_IMAGE_NAME` = $PRECISE_IMAGE_NAME ]; then
	echo "${PRECISE_IMAGE_NAME} already downloaded"
else
	echo "Downloading ${PRECISE_IMAGE_NAME}..."
	wget ${PRECISE_URL}
	echo "...Done"
fi

# Download the chef-server image
if [ `ls | grep $CHEF_IMAGE_NAME` = $CHEF_IMAGE_NAME ]; then
	echo "${CHEF_IMAGE_NAME} already downloaded"
else
	echo "Downloading ${CHEF_IMAGE_NAME}..."
	wget ${CHEF_IMAGE_URL}
	echo "...Done"
fi

# Once we have all we need, run the post-install.sh script
echo "CHMODing post-install.sh..."
chmod 0755 post-install.sh
echo "...Done"