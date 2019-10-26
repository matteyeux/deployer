# unused nvm will delete it
import docker


class RemoteDocker:
    def __init__(self, ip: str, port="2376"):
        self.ip = ip
        self.port = port

    def setup_docker_client(self):
        """return remote docker client instance"""
        self.a = docker.DockerClient(self.ip + ":" + self.port)

    def is_microservice_running(self, service_name: str) -> bool:
        for container in self.a.containers.list():
            if service_name == container.attrs["Name"].split('/')[1]:
                return True
        return False
