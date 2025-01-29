import sys
from typing import Optional, TextIO

from ..command import Command


class TypeCommand(Command):
    def execute(
        self,
        output_stream: Optional[TextIO] = sys.stdout,
        err_stream: Optional[TextIO] = sys.stderr,
    ):
        os = self._shell_ctx._utils.get_os()

        if self._args and isinstance(self._args, list):
            if self._args[0] in self._shell_ctx.get_built_in_commands():
                if output_stream:
                    output_stream.write(f"{self._args[0]} is a shell builtin\n")
            else:
                is_executable, exe_path = self._shell_ctx._utils.search_for_exe(
                    command=self._args[0]
                )
                if not is_executable:
                    if err_stream:
                        err_stream.write(f"{self._args[0]}: not found\n")
                else:
                    if output_stream:
                        output_stream.write(
                            f"{self._args[0]} is {os.path.normpath(exe_path)}\n"
                        )
