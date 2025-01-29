from .shell_utils import ShellUtils


class ShellContext:
    def __init__(self) -> None:
        self._built_ins: list[str] = [
            "exit",
            "echo",
            "type",
            "pwd",
            "cd",
        ]

        self._utils = ShellUtils()

    def get_built_in_commands(self) -> list[str]:
        return self._built_ins.copy()
