import sys
from typing import Optional, TextIO

from ..command import Command


class PwdCommand(Command):
    def execute(
        self,
        output_stream: Optional[TextIO] = sys.stdout,
        err_stream: Optional[TextIO] = sys.stderr,
    ) -> None:
        os = self._shell_ctx._utils.get_os()

        if output_stream:
            output_stream.write(os.getcwd() + "\n")
