import docker
from dataclasses import dataclass, field


@dataclass
class DockerClient:
    image: str

# client = docker.from_env()
# client.containers.run("ubuntu", "echo hello world",name="test")
# print(client.containers.list())