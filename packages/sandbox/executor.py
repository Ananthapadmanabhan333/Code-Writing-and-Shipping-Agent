import docker
import os
from typing import Dict, Any

class SandboxExecutor:
    def __init__(self):
        self.client = docker.from_env()

    def run_command(self, command: str, workdir: str, image: str = "python:3.11-slim") -> Dict[str, Any]:
        """
        Runs a command in an isolated Docker container.
        """
        try:
            container = self.client.containers.run(
                image=image,
                command=command,
                volumes={os.path.abspath(workdir): {'bind': '/app', 'mode': 'rw'}},
                working_dir='/app',
                detach=True,
                remove=True
            )
            result = container.wait()
            logs = container.logs().decode('utf-8')
            return {
                "status": "success" if result['StatusCode'] == 0 else "failed",
                "exit_code": result['StatusCode'],
                "logs": logs
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def run_test(self, test_command: str, workdir: str) -> Dict[str, Any]:
        return self.run_command(test_command, workdir)
