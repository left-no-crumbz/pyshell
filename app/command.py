import sys
from abc import ABC, abstractmethod
from typing import Optional, TextIO

from .shell_context import ShellContext


class Command(ABC):
    def __init__(
        self, shell_ctx: ShellContext, args: list[str] | str | None = None
    ) -> None:
        self._shell_ctx = shell_ctx
        self._args = args

    @abstractmethod
    def execute(
        self,
        output_stream: Optional[TextIO] = sys.stdout,
        error_stream: Optional[TextIO] = sys.stderr,
    ):
        pass
