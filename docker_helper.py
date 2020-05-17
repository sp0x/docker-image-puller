import logging
import subprocess
from subprocess import PIPE


class DockerHelper:
    logger = logging.Logger("docker")

    def __init__(self, pwd):
        self.dir = pwd

    def run_dc(self, command):
        whole_cmd = ["docker-compose"]
        whole_cmd.extend(command)
        whole_cmd = " ".join(whole_cmd)
        out = subprocess.run(whole_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.dir)
        print(out.stderr.decode("utf-8"))

    def pull(self, service):
        self.run_dc(["pull", service])

    def up(self, service, attach=False):
        self.run_dc(["up", "-d" if attach else "", service])

    def restart(self, service):
        self.run_dc(["restart", service])
