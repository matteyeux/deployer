# could be used to run docker container
#from another microservice
import os
import docker

docker_client = docker.DockerClient()

tag = 'my-hello-world'
context = os.path.abspath('.')
dockerfile = os.path.abspath(os.path.join('Dockerfile'))

print('Tag: {0}'.format(tag))
print('Context path: {0}'.format(context))
print('Dockerfile path: {0}'.format(dockerfile))

# This does not work
res = docker_client.images.build(tag=tag, path=context, dockerfile=dockerfile)

print('Successfully built image: {0}'.format(res))
