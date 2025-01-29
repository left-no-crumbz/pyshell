import sys
from typing import Optional, TextIO

from ..command import Command


class EchoCommand(Command):
    def parse(self, input_str: str) -> str:
        string = []
        idx = 0
        length = len(input_str)
        SPECIAL_CHARS = ["`", '"', "\\", "$"]
        in_quotes = False

        while idx < length:
            # handle SQ - preserve everything
            if input_str[idx] == "'":
                # get the next char
                idx += 1
                while idx < length and input_str[idx] != "'":
                    string.append(input_str[idx])
                    idx += 1

            # handle DQ - respect escape chars
            elif input_str[idx] == '"':
                in_quotes = not in_quotes
                # get the next char
                idx += 1

                while idx < length and input_str[idx] != '"':
                    if idx + 1 < length and (
                        (input_str[idx] == "\\" and input_str[idx + 1] in SPECIAL_CHARS)
                        or (
                            input_str[idx] == " "
                            and input_str[idx + 1] == " "
                            and not in_quotes
                        )
                    ):
                        # consume the curr char and append the next char
                        string.append(input_str[idx + 1])

                        idx += 2
                        continue

                    string.append(input_str[idx])
                    idx += 1

        return "".join(string)

    def execute(
        self,
        output_stream: Optional[TextIO] = sys.stdout,
        err_stream: Optional[TextIO] = sys.stderr,
    ) -> None:
        if not self._args:
            if output_stream:
                output_stream.write("\n")
            return

        if isinstance(self._args, str):
            string = self.parse(self._args)

            if output_stream:
                output_stream.write(string + "\n")
        else:
            has_backslash = False

            # check the string in the args if it has a backslash
            for element in self._args:
                for char in element:
                    if char == "\\":
                        has_backslash = True
                        break

            if has_backslash:
                if output_stream:
                    output_stream.write(" ".join(self._args).replace("\\", "") + "\n")

            else:
                if output_stream:
                    output_stream.write(
                        " ".join(
                            self._args if isinstance(self._args, list) else [self._args]
                        )
                        + "\n"
                    )
