#!/usr/bin/env python3
# TODO : run dockerfile sent by deployer.

from flask import Flask, jsonify
import docker

__author__ = 'hauteb_m'

app = Flask(__name__)

docker_client = docker.DockerClient("172.17.0.1:2376")


@app.route('/containers', methods=['GET'])
def run_dockerps_all() -> list:
	loop_list = []

	for c in docker_client.containers.list():
		loop_list.append(c.name)

	return jsonify(loop_list)


@app.route('/containers/<option>', methods=['GET'])
def run_dockerps(option) -> list:
	global_dict = {}

	for c in docker_client.containers.list():
		loop_list = []
		container_dict = {}

		container_dict["name"] = c.name
		container_dict["image"] = c.attrs["Config"]["Image"]
		container_dict["created"] = c.attrs["Created"]
		container_dict["id"] = c.id
		container_dict["short_hash"] = c.attrs["Config"]["Hostname"]
		
		if option == c.name or option == c.id:
			return jsonify(container_dict)

		loop_list.append(container_dict)

		global_dict[container_dict["name"]] = loop_list

	return jsonify(global_dict)


@app.errorhandler(404)
def page_not_found(error):
	return {'message': 'Not found'}, 404


@app.route('/')
def index():
	return "my_deployer\n"


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
