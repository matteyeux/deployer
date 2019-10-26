#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""my_deployer main file."""


import argparse
import argcomplete
import configparser
import docker_utils
import logging
import os
import paramiko
import subprocess
import sys

from docker_remote import RemoteDocker


__author__ = 'hauteb_m'


logging.basicConfig(filename="my_deployer.log",
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def deploy_info(config_file: str) -> list:
    """get server info for deployment"""
    srv_info = []
    ini = configparser.ConfigParser()
    ini.read(config_file)

    for info in ['host', 'port', 'user', 'password']:
        srv_info.append(ini['my_deployer'][info])
    return srv_info


def start_ssh(host_data, use_passwd=False):
    """setup paramiko and return it"""
    ssh_pub_key = os.environ["HOME"] + "/.ssh/etna_rsa"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if host_data[3] is None:
        ssh.connect(host_data[0], host_data[1], host_data[2],
                    key_filename=ssh_pub_key)
    else:
        ssh.connect(host_data[0], host_data[1], host_data[2], host_data[3])

    return ssh


def close_ssh(ssh):
    """close ssh connection"""
    try:
        ssh.close()
    except:
        raise("failed to close SSH connection")


def send_microservice(ssh, dir_name: str):
    """
    create remote dir
    send content of local dir
    to remote dir
    dir_name should have the same name
    than the microservice
    """
    sftp = ssh.open_sftp()
    target = os.environ['HOME'] + '/' + dir_name + '/'

    try:
        sftp.mkdir(dir_name)
    except:
        logging.info("failed, folder probably exists, skipping")

    for item in os.listdir(dir_name):
        real_item = dir_name + '/' + item
        sftp.put(real_item, target + item)

    sftp.close()


def parse_arguments():
    """argument parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", required=True, dest="server",
                        help="specify server IP")
    parser.add_argument("-p", "--port", dest="port", nargs=1,
                        help="specify server port")
    parser.add_argument("-u", "--user", dest="user", nargs=1,
                        help="specify user")
    parser.add_argument("-m", "--microservice", nargs='+', dest="microservice",
                        help="specify microservice")
    parser.add_argument("-c", "--config-file", dest="config_file",
                        help="credentials file (config.ini)")
    parser.add_argument("-k", "--healthcheck", action="store_true",
                        help="something with docker")

    argcomplete.autocomplete(parser)

    return parser.parse_args()


def main():
    """main function"""
    logging.info('Launching "{}", status: OK'.format(*sys.argv))

    # Password is set to None by default we use SSH key
    # default user is the current one
    srv_info = ["127.0.0.1", "22", os.environ["USER"], None]

    parser = parse_arguments()

    # in config file you can specify password
    # but not recommended
    if parser.config_file is not None:
        srv_info = deploy_info(parser.config_file)
    else:
        if parser.server is not None:
            srv_info[0] = parser.server

        if parser.port is not None:
            srv_info[1] = parser.port

        if parser.user is not None:
            srv_info[2] = parser.user

    ssh = start_ssh(srv_info)

    docker_check = docker_utils.is_dockerce_installed(ssh)

    if docker_check == 0:
        logging.info("all good, Docker is already installed")
    elif docker_check == 1:
        logging.info("upgrading docker")
        docker_utils.upgrade_docker(ssh)
    elif docker_check == 2:
        logging.info("installing docker")
        docker_utils.install_docker(ssh)
    else:
        pass

    # setup remote api
    docker_utils.setup_api_service(ssh)
    if parser.microservice is not None:
        microservice = parser.microservice
        for service in microservice:
            # check microservice
            # if microservice not up to date
            # run and clean or just run
            check = docker_utils.is_service_running(parser.server,
                                                    microservice)

            # TODO : check if container is up to date, not sure how to
            if check is True:
                logging.info("container already is running")
            else:
                logging.info("sending container %s" % service)
                send_microservice(ssh, service)
                logging.info("running container %s" % service)
                print("deploying {}".format(service))
                docker_utils.run_microservice(ssh, service)

    close_ssh(ssh)
    print("[i] deployment finished")


if __name__ == '__main__':
    main()
