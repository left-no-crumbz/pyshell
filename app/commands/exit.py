from ..command import Command


class ExitCommand(Command):
    def execute(
        self,
    ):
        sys = self._shell_ctx._utils.get_sys()
        sys.exit(0)
