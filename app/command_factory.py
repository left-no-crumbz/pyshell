from .commands.cat import CatCommand
from .commands.cd import CdCommand
from .commands.echo import EchoCommand
from .commands.exit import ExitCommand
from .commands.pwd import PwdCommand
from .commands.type import TypeCommand
from .shell_context import ShellContext


class CommandFactory:
    def __init__(self, shell_ctx: ShellContext) -> None:
        self._shell_ctx = shell_ctx
        self._commands = {
            "exit": ExitCommand,
            "echo": EchoCommand,
            "pwd": PwdCommand,
            "type": TypeCommand,
            "cd": CdCommand,
            "cat": CatCommand,
        }

    def create_command(
        self, command_name: str, args: list[str] | str | None = None
    ) -> None:
        # handle quoted executables
        if command_name.startswith("'") or command_name.startswith('"'):
            command_class = self._commands.get("cat")
        else:
            command_class = self._commands.get(command_name)

        if command_class:
            return command_class(self._shell_ctx, args)
        return None
