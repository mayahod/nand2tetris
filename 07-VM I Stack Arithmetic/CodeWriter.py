"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import os

PUSH = "@SP\n" + \
       "A=M\n" + \
       "M=D\n" + \
       "@SP\n" + \
       "M=M+1\n"


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_file = output_stream
        self.filename = ""
        self.unique_counter = 0


    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        input_filename, input_extension = os.path.splitext(os.path.basename(filename))
        self.filename = input_filename

    def two_arguments(self, operation: str) -> str:
        result = "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "M=M" + operation + "D\n" + \
                 "@SP\n" + \
                 "M=M+1\n"
        return result

    def one_argument(self, operation: str) -> str:
        result = "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "M=" + operation + "M\n" + \
                 "@SP\n" + \
                 "M=M+1\n"
        return result


    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        result = "invalid_command"
        if (command == "add"):
            result = self.two_arguments('+')
        elif (command == "sub"):
            result = self.two_arguments('-')
        elif (command == "neg"):
            result = self.one_argument('-')
        elif command in {"eq", "gt", "lt"}:
            result = self.compare(command.upper())
        elif (command == "and"):
            result = self.two_arguments('&')
        elif (command == "or"):
            result = self.two_arguments('|')
        elif (command == "not"):
            result = self.one_argument('!')
        elif (command == "shiftleft"):
            result = self.one_argument("<<")
        elif (command == "shiftright"):
            result = self.one_argument(">>")
        self.output_file.write(result)


    def compare(self, command: str):
        self.unique_counter += 1
        result = "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@R13\n" + \
                 "M=D\n" + \
                 "@yNEGETIVE" + str(self.unique_counter) + "\n" + \
                 "D;JLT\n" + \
                 "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@xNEGyPOS" + str(self.unique_counter) + "\n" + \
                 "D;JLT\n" + \
                 "@R13\n" + \
                 "D=D-M\n" + \
                 "@VALUE" + str(self.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(yNEGETIVE" + str(self.unique_counter) + ")\n" + \
                 "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@xPOSyNEG" + str(self.unique_counter) + "\n" + \
                 "D;JGT\n" + \
                 "@R13\n" + \
                 "D=D-M\n" + \
                 "@VALUE" + str(self.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(xPOSyNEG" + str(self.unique_counter) + ")\n" + \
                 "D=1\n" + \
                 "@VALUE" + str(self.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(xNEGyPOS" + str(self.unique_counter) + ")\n" + \
                 "D=-1\n" + \
                 "@VALUE" + str(self.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(VALUE" + str(self.unique_counter) + ")\n" + \
                 "@TRUE" + str(self.unique_counter) + "\n" + \
                 "D;J" + command + "\n" + \
                 "D=0\n" + \
                 "@LAST" + str(self.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(TRUE" + str(self.unique_counter) + ")\n" + \
                 "D=-1\n" + \
                 "@LAST" + str(self.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(LAST" + str(self.unique_counter) + ")\n" + \
                 "@SP\n" + \
                 "A=M\n" + \
                 "M=D\n" + \
                 "@SP\n" + \
                 "M=M+1\n"
        return result

    def compare_org(self, command: str):
        jump_label = "JUMP_" + str(self.unique_counter)
        self.unique_counter += 1
        result = "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@R13\n" + \
                 "M=D\n" + \
                 "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M-D\n" + \
                 "@" + jump_label + "\n" + \
                 "D;J" + command.upper() + "\n" + \
                 "@SP\n" + \
                 "A=M\n" + \
                 "M=0\n" + \
                 "@END_" + jump_label + "\n" + \
                 "0;JMP\n" + \
                 "(" + jump_label + ")\n" + \
                 "@SP\n" + \
                 "A=M\n" + \
                 "M=-1\n" + \
                 "(END_" + jump_label + ")\n" + \
                 "@SP\n" + \
                 "M=M+1\n"
        return result

    memory_segment = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT",
                      "static": "16", "pointer": "3", "temp": "5"}

    def get_memory(self, segment: str):
        return self.memory_segment.get(segment, "UNKNOWN_SEGMENT")

    def push1(self, segment: str, index: int):
        push = 'invalid_segment'
        if (segment == "constant"):
            push = "@" + str(index) + "\n" + \
                   "D=A\n" + \
                   "@SP\n" + \
                   "A=M\n" + \
                   "M=D\n" + \
                   "@SP\n" + \
                   "M=M+1\n"
        elif segment in {"local", "argument", "this", "that"}:
            push = "@" + str(index) + "\n" + \
                   "D=A\n" + \
                   "@" + self.get_memory(segment) + "\n" + \
                   "A=M+D\n" + \
                   "D=M\n" + \
                   PUSH
        elif (segment == "temp" ):
            push = "@" + str(index) + "\n" + \
                   "D=A\n" + \
                   "@" + self.get_memory(segment) + "\n" + \
                   "D=D+A\n" + \
                   "A=D\n" + \
                   "D=M\n" + \
                   PUSH
        #elif (segment == "pointer"):
        #    push = "@1\n" + \
        #           "D=A\n" + \
        #           "@" + str(index) + "\n" + \
        #           "D=D-A\n" + \
        #           "@THAT1\n" + \
        #           "D;JEQ\n" + \
        #           "@THIS1\n" + \
        #           "D;JGT\n" + \
        #           "(THAT1)\n" + \
        #           "@THAT\n" + \
        #           "D=M\n" + \
        #           PUSH + \
        #           "(THIS1)\n" + \
        #           "@THIS\n" + \
        #           "D=M\n" + \
        #           PUSH
        elif (segment == "pointer"):
            push = "@R" + str((int(index)) + int(self.get_memory(segment))) + "\n" + \
                   "D=M\n" + PUSH
        elif (segment == "static"):
            push = "@" + self.filename + "." + str(index) + "\n" + \
                   "D=M\n" + \
                   "@SP\n" + \
                   "A=M\n" + \
                   "M=D\n" + \
                   "@SP\n" + \
                   "M=M+1\n"
        return push


    def pop1(self, segment: str, index: int):
        pop = ''
        if (segment in {"argument", "that", "this","local"}):
            pop = "@" + str(index) + "\n" + \
                  "D=A\n" + \
                  "@" + self.get_memory(segment) + "\n" + \
                  "A=M\n" + \
                  "D=A+D\n" + \
                  "@R13\n" + \
                  "M=D\n" + \
                  "@SP\n" + \
                  "M=M-1\n" + \
                  "@SP\n" + \
                  "A=M\n" + \
                  "D=M\n" + \
                  "@R13\n" + \
                  "A=M\n" + \
                  "M=D\n"
        elif (segment == "pointer" or segment == "temp"):
            pop = "@SP\n" + \
                  "M=M-1\n" + \
                  "A=M\n" + \
                  "D=M\n" + \
                  "@R" + str(index + int(self.get_memory(segment))) + "\n" + \
                  "M=D\n"
        elif (segment == "static"):
            pop = "@SP\n" + \
                  "M=M-1\n" + \
                  "A=M\n" + \
                  "D=M\n" + \
                  "@" + self.filename + "." + str(index) + "\n" + \
                  "M=D\n"
        return pop

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if (command == "C_PUSH"):
            result = self.push1(segment, index)
        elif (command == "C_POP"):
            result = self.pop1(segment, index)
        self.output_file.write(result)

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
