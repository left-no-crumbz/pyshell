from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class ParsedInput:
    command_name: str
    args: Optional[Union[list[str], str]] = None
    redirect_to_stdout: Optional[str] = None
    redirect_to_stderr: Optional[str] = None
    is_quoted_command: bool = False
    redirection_symbol: Optional[str] = None


class InputParser:
    @staticmethod
    def split_redirection(
        input_line: str,
    ) -> tuple[str, Optional[str], Optional[str], Optional[str]]:
        stdout_redirect = None
        stderr_redirect = None
        redirection_symbol = None

        if "1>>" in input_line:
            input_line, stdout_redirect = input_line.split("1>>", 1)
            stdout_redirect = stdout_redirect.strip()
            redirection_symbol = "1>>"

        if "2>>" in input_line:
            input_line, stderr_redirect = input_line.split("2>>", 1)
            stderr_redirect = stderr_redirect.strip()
            redirection_symbol = "2>>"

        if ">>" in input_line:
            input_line, stdout_redirect = input_line.split(">>", 1)
            stdout_redirect = stdout_redirect.strip()
            redirection_symbol = ">>"

        if "2>" in input_line:
            input_line, stderr_redirect = input_line.split("2>", 1)
            stderr_redirect = stderr_redirect.strip()
            redirection_symbol = "2>"

        if "1>" in input_line:
            input_line, stdout_redirect = input_line.split("1>", 1)
            stdout_redirect = stdout_redirect.strip()
            redirection_symbol = "1>"

        elif ">" in input_line:
            input_line, stdout_redirect = input_line.split(">", 1)
            stdout_redirect = stdout_redirect.strip()
            redirection_symbol = ">"

        return input_line.strip(), stdout_redirect, stderr_redirect, redirection_symbol

    @staticmethod
    def parse_quoted_command(input_str: str) -> tuple[str, Optional[str]]:
        quote_char = input_str[0]
        remaining = iter(input_str[1:])

        command_parts = []
        args_parts = []
        in_quotes = True

        for char in remaining:
            if char == quote_char:
                in_quotes = not in_quotes
                continue
            if in_quotes:
                command_parts.append(char)
            else:
                args_parts.append(char)

        command = quote_char + "".join(command_parts) + quote_char
        args = "".join(args_parts).strip()

        return command, args if args else None

    def parse(self, input_line: str) -> ParsedInput:
        if not input_line.strip():
            return ParsedInput("")

        command_part, stdout_redirect, stderr_redirect, redirection_symbol = (
            self.split_redirection(input_line)
        )

        # handle quoted executables
        if command_part.startswith(("'", '"')):
            command_name, args = self.parse_quoted_command(command_part)
            return ParsedInput(
                command_name=command_name,
                args=args,
                redirect_to_stdout=stdout_redirect,
                redirect_to_stderr=stderr_redirect,
                is_quoted_command=True,
                redirection_symbol=redirection_symbol,
            )
        parts = command_part.split(maxsplit=1)
        command_name = parts[0]

        # handle commands like `pwd`
        if len(parts) == 1:
            return ParsedInput(
                command_name=command_name,
                redirect_to_stdout=stdout_redirect,
                redirect_to_stderr=stderr_redirect,
                redirection_symbol=redirection_symbol,
            )

        args_part = parts[1]
        # handle quoted args for commands like `echo`
        if args_part.startswith(("'", '"')):
            return ParsedInput(
                command_name=command_name,
                args=args_part,
                redirect_to_stdout=stdout_redirect,
                redirect_to_stderr=stderr_redirect,
                redirection_symbol=redirection_symbol,
            )

        # catch all parsed input
        # typically for echo commands that aren't quoted
        return ParsedInput(
            command_name=command_name,
            args=args_part.split(),
            redirect_to_stdout=stdout_redirect,
            redirect_to_stderr=stderr_redirect,
            redirection_symbol=redirection_symbol,
        )
