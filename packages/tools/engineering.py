import os
import subprocess
from typing import List, Dict, Any
from packages.sandbox.executor import SandboxExecutor

class EngineeringTools:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.sandbox = SandboxExecutor()

    def write_file(self, path: str, content: str):
        full_path = os.path.join(self.base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return f"File written to {path}"

    def read_file(self, path: str) -> str:
        full_path = os.path.join(self.base_dir, path)
        with open(full_path, "r") as f:
            return f.read()

    def list_files(self, path: str = ".") -> List[str]:
        full_path = os.path.join(self.base_dir, path)
        return os.listdir(full_path)

    def run_in_sandbox(self, command: str, image: str = "python:3.11-slim") -> Dict[str, Any]:
        return self.sandbox.run_command(command, self.base_dir, image)

    def git_commit(self, message: str):
        # Mock git commit for now
        return f"Committed with message: {message}"
