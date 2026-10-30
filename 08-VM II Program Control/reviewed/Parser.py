"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing


class Parser:
    """Parses one VM file and exposes the current command and its arguments."""

    ARITHMETIC_COMMANDS = {
        "add", "sub", "neg", "eq", "gt", "lt",
        "and", "or", "not", "shiftleft", "shiftright",
    }

    COMMAND_TYPES = {
        "push": "C_PUSH",
        "pop": "C_POP",
        "label": "C_LABEL",
        "goto": "C_GOTO",
        "if-goto": "C_IF",
        "function": "C_FUNCTION",
        "return": "C_RETURN",
        "call": "C_CALL",
    }

    def __init__(self, input_file: typing.TextIO) -> None:
        """Read and normalize all meaningful VM lines."""
        self.commands = []

        for raw_line in input_file.read().splitlines():
            command = raw_line.split("//", 1)[0].strip()
            if command:
                self.commands.append(" ".join(command.split()))

        self.current_index = 0
        self.current_command = ""

    def has_more_commands(self) -> bool:
        """Return True when another VM command is available."""
        return self.current_index < len(self.commands)

    def advance(self) -> None:
        """Advance to the next VM command."""
        if not self.has_more_commands():
            raise StopIteration("No more VM commands.")

        self.current_command = self.commands[self.current_index]
        self.current_index += 1

    def _parts(self) -> list[str]:
        if not self.current_command:
            raise ValueError("No current command.")
        return self.current_command.split()

    def command_type(self) -> str:
        """Return the VM command category for the current command."""
        command = self._parts()[0]

        if command in self.ARITHMETIC_COMMANDS:
            return "C_ARITHMETIC"

        try:
            return self.COMMAND_TYPES[command]
        except KeyError as error:
            raise ValueError(f"Unknown VM command: {command}") from error

    def arg1(self) -> str:
        """Return the first argument, or the arithmetic command itself."""
        parts = self._parts()
        command_type = self.command_type()

        if command_type == "C_RETURN":
            raise ValueError("C_RETURN has no first argument.")

        if command_type == "C_ARITHMETIC":
            return parts[0]

        if len(parts) < 2:
            raise ValueError(f"Missing first argument: {self.current_command}")

        return parts[1]

    def arg2(self) -> int:
        """Return the numeric second argument for commands that have one."""
        if self.command_type() not in {
            "C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"
        }:
            raise ValueError(
                f"Command has no second argument: {self.current_command}")

        parts = self._parts()
        if len(parts) < 3:
            raise ValueError(f"Missing second argument: {self.current_command}")

        try:
            value = int(parts[2])
        except ValueError as error:
            raise ValueError(
                f"Second argument must be an integer: {self.current_command}"
            ) from error

        if value < 0:
            raise ValueError(
                f"Second argument must be non-negative: {self.current_command}")

        return value
