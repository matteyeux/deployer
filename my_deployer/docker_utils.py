#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Docker stuff"""

import logging
import paramiko
import requests
import time

__author__ = "hauteb_m"


def is_dockerce_installed(ssh) -> int:
    """check if docker-ce is installed
    0 : OK
    1 : have to upgrade/downgrade
    2 : have to install
    """
    (stdin, stdout, stderr) = ssh.exec_command("dpkg -l")
    for pkg in stdout.readlines():
        if "docker-ce-cli" in pkg and "19.03" in pkg:
            return 0
        elif "docker-ce-cli" in pkg and "19.03" not in pkg:
            return 1
        else:
            pass
    return 2


def install_docker(ssh):
    """
    install Docker on remote host
    I use sudo for install so in /etc/sudoers :
    username     ALL=(ALL) NOPASSWD:ALL
    """
    commands = [
        "sudo apt update",
        "sudo apt install -y apt-transport-https \
         ca-certificates curl gnupg2 software-properties-common",
        "curl -fsSL https://download.docker.com/linux/debian/gpg |\
         sudo apt-key add -",
        "sudo apt-key fingerprint 0EBFCD88"
        "sudo add-apt-repository 'deb [arch=amd64] \
        https://download.docker.com/linux/debian buster stable'",
        "sudo apt update",
        "sudo apt install -y 'docker-ce=5:19.03.4~3-0~debian-buster'\
         docker-ce-cli containerd.io",
    ]

    for command in commands:
        ssh.exec_command(command)


def upgrade_docker(ssh):
    """upgrade Docker on remote host"""
    ssh.exec_command("sudo apt install docker-ce=5:19.03.4~3-0~debian-buster")


def setup_api_service(ssh):
    """setup api on deployer VM"""
    command = "docker-compose -f checker/docker-compose.yml up -d"

    logging.info("starting API, may take a while")
    (stdin, stdout, stderr) = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()

    logging.info("exit status command {} : {}".format(command, exit_status))


def run_microservice(ssh, service: str):
    """
    run microservice on remote host
    TODO use docker module
    """
    # build
    command = "docker build -t {} .".format(service)
    logging.info("running {}".format(command))

    (stdin, stdout, stderr) = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    logging.info("done")

    # run as detached
    command = "docker run -d -t {}".format(service)
    logging.info("running {}".format(command))

    (stdin, stdout, stderr) = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    logging.info("done")


def is_service_running(server: str, service: str) -> bool:
    api_endpoint = "http://" + server + ":5000/containers"
    logging.info("waiting 3 seconds for stuff to setup")
    time.sleep(1)

    r = requests.get(api_endpoint).json()

    for container in r:
        if container == service:
            return True
    return False
