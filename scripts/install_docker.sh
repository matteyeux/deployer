#!/bin/bash
# script to install Docker
# because flemme

sudo apt-get update

sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common -y

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io -y

# allow to run without being root
sudo usermod -aG docker mathieu
