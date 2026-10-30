"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

import re


class Parser:
    """
    # Parser

    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient
    access to their components.
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line's end. 
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that,
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        input_lines = input_file.read().splitlines()
        input_lines = [re.sub(r'\s*//.*', '', line).strip() for line in input_lines]
        input_lines = [' '.join(line.split()) for line in input_lines if line]
        self.input_lines = input_lines
        self.current_line = 0
        self.current_command = ''

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return (self.current_line < len(self.input_lines))

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        if (self.has_more_commands()):
            self.current_command = self.input_lines[self.current_line]
            self.current_line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        if ((self.current_command.startswith("add")) or (self.current_command.startswith("sub")) or
                (self.current_command.startswith("neg")) or (self.current_command.startswith("eq"))
                or (self.current_command.startswith("gt")) or (self.current_command.startswith("lt"))
                or (self.current_command.startswith("and")) or (self.current_command.startswith("or")) or
                (self.current_command.startswith("not")) or (self.current_command.startswith("shiftleft"))
                or (self.current_command.startswith("shiftright"))):
            return "C_ARITHMETIC"
        elif (self.current_command.startswith("push")):
            return "C_PUSH"
        elif (self.current_command.startswith("pop")):
            return "C_POP"
        elif (self.current_command.startswith("label")):
            return "C_LABEL"
        elif (self.current_command.startswith("if")):
            return "C_IF"
        elif (self.current_command.startswith("goto")):
            return "C_GOTO"
        elif (self.current_command.startswith("function")):
            return "C_FUNCTION"
        elif (self.current_command.startswith("return")):
            return "C_RETURN"
        elif (self.current_command.startswith("call")):
            return "C_CALL"
        return ""

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned.
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        if (self.command_type() != "C_RETURN"):
            parts = self.current_command.split()
            return parts[1] if len(parts) > 1 else ""
        return ""

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP",
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        if (self.command_type() in {"C_PUSH", "C_POP",
                                    "C_FUNCTION", "C_CALL"}):
            parts = self.current_command.split()
            return int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        return 0