import re
from dataclasses import dataclass

from testcontainers.compose import DockerCompose as BaseDockerCompose


@dataclass
class DockerCompose(BaseDockerCompose):
    def kill(self) -> None:
        """
        Stops the docker compose environment with timeout 0
        """
        down_cmd = self.compose_command_property[:]
        down_cmd += ["down", "--volumes", "-t", "0"]
        self._run_command(cmd=down_cmd)


def wait_for_logs(compose: DockerCompose, regex: str) -> list[str]:
    while True:
        stdout, stderr = compose.get_logs()

        if m := re.findall(regex, stdout):
            return m
