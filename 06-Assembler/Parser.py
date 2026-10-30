import typing

import re


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        #input_lines = input_file.read().splitlines()
        input_lines = input_file.read().splitlines()
        #input_lines = [line.replace('\n', '') for line in input_lines] #removes '\n'
        #input_lines = [line.strip() for line in input_lines] #removes leading and trailing whitespace
        #input_lines = [re.sub(r'//.*', '', line) for line in input_lines] #removes comments line
        #input_lines = [line for line in input_lines if line] # delete the empty lines
        #input_lines = input_file.readlines()
        input_lines = [re.sub(r'\s*//.*', '', line).strip() for line in input_lines]
        #input_lines = [line for line in input_lines if line]
        input_lines = [line.replace(" ", "") for line in input_lines if line]
        # input_lines = [line.strip() for line in input_lines if line and not line.startswith('//')]
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
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        # Your code goes here!
        if (self.has_more_commands()):
            self.current_command = self.input_lines[self.current_line]
            self.current_line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        if (self.current_command.startswith("@")):
            return "A_COMMAND"
        elif (("(" in self.current_command) and (")" in self.current_command)):
            return "L_COMMAND"
        elif (("=" in self.current_command) or (";" in self.current_command)):
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or
            "L_COMMAND".
        """
        # Your code goes here!
        if (self.command_type() == "L_COMMAND") or (self.command_type() == "A_COMMAND"):
            if (self.command_type() == "A_COMMAND"):
                return self.current_command.replace("@", "")
            if (self.command_type() == "L_COMMAND"):
                return self.current_command.replace("(", "").replace(")", "")
        return ''

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if (self.command_type() == "C_COMMAND"):
            return self.current_command.split('=')[0]
        return ''

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if self.command_type() == "C_COMMAND":
            parts = re.split('[=;]', self.current_command)
            if len(parts) == 3:
                return parts[1]
            elif len(parts) == 2:
                return parts[1] if '=' in self.current_command else parts[0]
        return ''

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        # Your code goes here!
        if (self.command_type() == "C_COMMAND"):
            parts = self.current_command.split(';')
            if (len(parts) == 2):
                return parts[1]
            else:
                return ''
        return ''