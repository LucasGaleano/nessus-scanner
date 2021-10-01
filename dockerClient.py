import docker
from dataclasses import dataclass, field


@dataclass
class DockerClient:
    image: str

    def start(self, port):
        client = docker.from_env()
        print(client)
        print('[+] start container', self.image)
        container = client.containers.run(self.image, detach=True, auto_remove=True, ports={'8834/tcp': port})
        print('[+] container started', self.image)
        return container


# 
# client.containers.run("ubuntu", "echo hello world",name="test")
# print(client.containers.list())