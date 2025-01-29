import sys
from typing import Optional, TextIO

from ..command import Command


class CdCommand(Command):
    def execute(
        self,
        output_stream: Optional[TextIO] = sys.stdout,
        err_stream: Optional[TextIO] = sys.stderr,
    ):
        os = self._shell_ctx._utils.get_os()

        if not self._args or not isinstance(self._args, list):
            if err_stream:
                err_stream.write("cd: missing directory argument\n")
            return

        try:
            target_path = (
                os.environ.get("HOME") if self._args[0] == "~" else self._args[0]
            )

            os.chdir(target_path)
        except FileNotFoundError:
            if err_stream:
                err_stream.write(f"cd: {self._args[0]}: No such file or directory\n")
