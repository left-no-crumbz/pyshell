import os
import subprocess
import sys
from typing import Any


class ShellUtils:
    @classmethod
    def get_os(cls) -> Any:
        return os

    @classmethod
    def get_sys(cls) -> Any:
        return sys

    @classmethod
    def get_subprocess(cls) -> Any:
        return subprocess

    @staticmethod
    def search_for_exe(command: str) -> tuple[bool, str]:
        env = os.environ.get("PATH")

        if env:
            paths = env.split(os.pathsep)
        else:
            print("[WARN]: env is None")

        for outerpath in paths:
            for (
                root,
                _,
                _,
            ) in os.walk(outerpath):
                path = os.path.join(root, command)
                if os.access(path, os.X_OK):
                    return True, path
        return False, ""

    @staticmethod
    def get_exe_list() -> list[str]:
        executables = set()

        env = os.environ.get("PATH")

        if env:
            paths = env.split(os.pathsep)
        else:
            print("[WARN]: env is None")

        for path in paths:
            if os.path.isdir(path):
                executables.update(os.listdir(path))

        return sorted(executables)
