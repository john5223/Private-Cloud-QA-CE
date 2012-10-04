#!/bin/bash

## This is a script that is run locally to prepare a server for installing alamo
## Author : Solomon Wagner

## CREATE NEEDED DIRECTORIES
# make the /opt/rpcs directory and move into it
mkdir -p /opt/rpcs
cd /opt/rpcs

# Get the hostname of the server
echo "Gathering name of the current host"
HOSTNAME = hostname

## GATHER DEFAULT IMAGES
# Image URLS
# Might make the parameters in the future
CIRROS_IMAGE_NAME="cirros-0.3.0-x86_64-uec.tar.gz"
CIRROS_URL="https://launchpadlibrarian.net/83305869/${CIRROS_IMAGE_NAME}"
PRECISE_IMAGE_NAME="precise-server-cloudimg-amd64.tar.gz"
PRECISE_URL="http://cloud-images.ubuntu.com/precise/current/${PRECISE_IMAGE_NAME}"

# Our File Server URLS
FILE_SERVER_URL="http://198.61.203.76/alamo"
POST_INSTALL_LOCATION="post-install.sh"
FUNCTIONS_LOCATION="functions.sh"
RPCS_CFG_LOCATION="${HOSTNAME}-rpcs.cfg"

## Gather the resource files that we need 
# Download the cirros image
echo "Downloading Cirros Image"
wget ${CIRROS_URL}

# Download the precise image
echo "Downloading Precise Image"
wget ${PRECISE_URL}

# Download post-install.sh
echo "Downloading post-install.sh"
wget "${FILE_SERVER_URL}/${POST_INSTALL_LOCATION}"

# Download functions.sh
echo "Downloading functions.sh"
wget "${FILE_SERVER_URL}/${FUNCTIONS_LOCATION}"

# Download the rpcs.cfg file for this hostname
echo "Downloading ${HOSTNAME}-rpcs.cfg"
wget "${FILE_SERVER_URL}/${RPCS_CFG_LOCATION}"

# Create rpcs.cfg
echo "Creating rpcs.cfg"
cp "${HOSTNAME}-rpcs.cfg" rpcs.cfg

# Delete old rpcs.cfg
echo "Deleting ${HOSTNAME}-rpcs.cfg"
rm -r "${HOSTNAME}-rpcs.cfg"

# Once we have all we need, run the post-install.sh script
chmod +x post-install.sh
./post-install.sh