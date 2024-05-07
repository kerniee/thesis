import re

from testcontainers.compose import DockerCompose


def wait_for_logs(compose: DockerCompose, regex: str) -> list[str]:
    while True:
        stdout, stderr = compose.get_logs()

        if m := re.findall(regex, stdout):
            return m
