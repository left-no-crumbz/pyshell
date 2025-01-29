# cat.py
import sys
from typing import Iterator, Optional, TextIO

from ..command import Command


class CatCommand(Command):
    def parse(self, input_str: str) -> list[str]:
        return list(self.parse_generator(input_str))

    def parse_generator(self, input_str: str):
        chars = iter(input_str)
        token = []

        while True:
            try:
                char = next(chars)
                match char:
                    # preserve everything
                    case "'":
                        quoted_content = self.parse_quote("'", False, chars)
                        token.append(quoted_content)
                    # allow escapes
                    case '"':
                        quoted_content = self.parse_quote('"', True, chars)
                        token.append(quoted_content)
                    case " ":
                        if token:  # only yield non-empty tokens
                            yield "".join(token)
                            token = []
                    case "\\":
                        try:
                            next_char = next(chars)
                            token.append("\\" + next_char)
                        except StopIteration:
                            token.append(char)
                    case char:
                        token.append(char)
            except StopIteration:
                if token:
                    yield "".join(token)
                break

    def parse_quote(self, until: str, allow_escape: bool, chars: Iterator[str]) -> str:
        token = []
        while True:
            try:
                char = next(chars)
                if char == until:
                    break

                # preserve everything
                if not allow_escape:
                    token.append(char)
                    continue

                # allow escapes
                if char == "\\" and allow_escape:
                    try:
                        next_char = next(chars)
                        if next_char in ["\\", "$", '"']:
                            token.append(next_char)
                        else:
                            token.append(char)
                            token.append(next_char)
                    except StopIteration:
                        token.append(char)
                        break
                else:
                    token.append(char)
            except StopIteration:
                break

        return "".join(token)

    def execute(
        self,
        output_stream: Optional[TextIO] = sys.stdout,
        err_stream: Optional[TextIO] = sys.stderr,
    ) -> None:
        if not self._args:
            if output_stream:
                output_stream.write("\n")
            return

        file_paths = []

        if isinstance(self._args, str):
            file_paths = self.parse(self._args)
        elif isinstance(self._args, list):
            for arg in self._args:
                file_paths.extend(self.parse(arg))

        for path in file_paths:
            try:
                with open(path, "r") as file:
                    for line in file:
                        if output_stream:
                            output_stream.write(line)

            except FileNotFoundError:
                if err_stream:
                    err_stream.write(f"cat: {path}: No such file or directory\n")

        # if output_stream:
        #     output_stream.write("".join(content))
