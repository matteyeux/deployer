#!/bin/bash
##############################
# script to bind docker daemon 
# on 0.0.0.0:2376 at boot
# test on Debian Buster
#############################

if [[ $(whoami) != "root" ]]; then
	echo "run as root"
	exit 1
fi

mkdir -p /etc/systemd/system/docker.service.d

echo "# /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2376
" > /etc/systemd/system/docker.service.d/startup_options.conf


systemctl daemon-reload
systemctl restart docker.service
