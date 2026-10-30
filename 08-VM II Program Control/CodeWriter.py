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
    unique_counter = 0
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
        self.file_name = ""
        self.label_func = ""
        self.operators = {"add": "+", "sub": "-", "neg": "-", "eq": "JNE",
                          "gt": "JLE", "lt": "JGE", "and": "&", "or": "|",
                          "not": "!"}
        self.memory_segment = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT",
                               "pointer": "3", "temp": "5", "static":"16"}

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
        #input_filename, input_extension = os.path.splitext(os.path.basename(filename.name))
        # input_filename, input_extension = os.path.splitext(os.path.basename(filename.name))
        # self.file_name = input_filename
        input_filename = os.path.splitext(os.path.basename(filename))[0]
        self.file_name = input_filename


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
         result = ""
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
             result = self.one_argument('<<')
         elif (command == "shiftright"):
             result = self.one_argument('>>')
         self.output_file.write(result)

    def compareOp(self, command):
        CodeWriter.unique_counter += 1
        commandStr = "@SP\n" + \
                     "M = M - 1\n" + \
                     "A = M\n" + \
                     "D = M\n" + \
                     "@R13\n" + \
                     "M = D\n" + \
                     "@yNeg" + str(CodeWriter.unique_counter) + "\n" + \
                     "D;JLT\n" + \
                     "@SP\n" + \
                     "M = M - 1\n" + \
                     "A = M\n" + \
                     "D = M\n" + \
                     "@yPosXNeg" + str(CodeWriter.unique_counter) + "\n" + \
                     "D;JLT\n" + \
                     "@R13\n" + \
                     "D = D - M\n" + \
                     "@CHECK" + str(CodeWriter.unique_counter) + "\n" + \
                     "0;JMP\n" + \
                     "(yNeg" + str(CodeWriter.unique_counter) + ")\n" + \
                     "@SP\n" + \
                     "M = M - 1\n" + \
                     "A = M\n" + \
                     "D = M\n" + \
                     "@yNegXPos" + str(CodeWriter.unique_counter) + "\n" + \
                     "D;JGT\n" + \
                     "@R13\n" + \
                     "D = D - M\n" + \
                     "@CHECK" + str(CodeWriter.unique_counter) + "\n" + \
                     "0;JMP\n" + \
                     "(yPosXNeg" + str(CodeWriter.unique_counter) + ")\n" + \
                     "D = -1\n" + \
                     "@CHECK" + str(CodeWriter.unique_counter) + "\n" + \
                     "0;JMP\n" + \
                     "(yNegXPos" + str(CodeWriter.unique_counter) + ")\n" + \
                     "D = 1\n" + \
                     "@CHECK" + str(CodeWriter.unique_counter) + "\n" + \
                     "0;JMP\n" + \
                     "(CHECK" + str(CodeWriter.unique_counter) + ")\n" + \
                     "@ISTRUE" + str(CodeWriter.unique_counter) + "\n" + \
                     "D;J" + command.upper() + "\n" + \
                     "D = 0\n" + \
                     "@AFTER" + str(CodeWriter.unique_counter) + "\n" + \
                     "0;JMP\n" + \
                     "(ISTRUE" + str(CodeWriter.unique_counter) + ")\n" + \
                     "D = -1\n" + \
                     "@AFTER" + str(CodeWriter.unique_counter) + "\n" + \
                     "0;JMP\n" + \
                     "(AFTER" + str(CodeWriter.unique_counter) + ")\n" + \
                     "@SP\n" + \
                     "A = M\n" + \
                     "M = D\n" + \
                     "@SP\n" + \
                     "M = M + 1\n"
        return commandStr

    def comp_op(self, command):
        CodeWriter.unique_counter += 1
        to_write = "// " + command + " command\n" + "@SP\n" + "AM=M-1\n" + "D=M\n" + \
                   "A=A-1\n" + "D=M-D\n" + "@FALSE" + str(CodeWriter.unique_counter) + "\n" + \
                   "D;" + self.operators[command] + "\n" + "@SP\n" + "A=M-1\n" + \
                   "M=-1\n" + "@CONTINUE" + str(CodeWriter.unique_counter) + "\n" + \
                   "0;JMP\n" + "(FALSE" + str(CodeWriter.unique_counter) + ")\n" + \
                   "@SP\n" + "A=M-1\n" + \
                   "M=0\n" + "(CONTINUE" + str(CodeWriter.unique_counter) + ")\n"
        return to_write

    def compare(self, command: str):
        CodeWriter.unique_counter += 1
        result = "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@R13\n" + \
                 "M=D\n" + \
                 "@ynegetive" + str(CodeWriter.unique_counter) + "\n" + \
                 "D;JLT\n" + \
                 "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@xnegypos" + str(CodeWriter.unique_counter) + "\n" + \
                 "D;JLT\n" + \
                 "@R13\n" + \
                 "D=D-M\n" + \
                 "@commend" + str(CodeWriter.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(ynegetive" + str(CodeWriter.unique_counter) + ")\n" + \
                 "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@xposyneg" + str(CodeWriter.unique_counter) + "\n" + \
                 "D;JGT\n" + \
                 "@R13\n" + \
                 "D=D-M\n" + \
                 "@commend" + str(CodeWriter.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(xposyneg" + str(CodeWriter.unique_counter) + ")\n" + \
                 "D=-1\n" + \
                 "@commend" + str(CodeWriter.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(xnegypos" + str(CodeWriter.unique_counter) + ")\n" + \
                 "D=0\n" + \
                 "@commend" + str(CodeWriter.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(commend" + str(CodeWriter.unique_counter) + ")\n" + \
                 "@TRUE" + str(CodeWriter.unique_counter) + "\n" + \
                 "D;J" + command + "\n" + \
                 "D=0\n" + \
                 "@LAST" + str(CodeWriter.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(TRUE" + str(CodeWriter.unique_counter) + ")\n" + \
                 "D=-1\n" + \
                 "@LAST" + str(CodeWriter.unique_counter) + "\n" + \
                 "0;JMP\n" + \
                 "(LAST" + str(CodeWriter.unique_counter) + ")\n" + \
                 "@SP\n" + \
                 "A=M\n" + \
                 "M=D\n" + \
                 "@SP\n" + \
                 "M=M+1\n"
        return result



    def compare_org(self, command: str):
        jump_label = "JUMP_" + str(CodeWriter.unique_counter)
        CodeWriter.unique_counter += 1
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
                   "D=D+M\n" + \
                   "A=D\n" + \
                   "D=M\n" + \
                   PUSH
        elif (segment == "temp"):
            push = "@" + str(index) + "\n" + \
                   "D=A\n" + \
                   "@" + self.get_memory(segment) + "\n" + \
                   "D=D+A\n" + \
                   "A=D\n" + \
                   "D=M\n" + \
                   PUSH
        # elif (segment == "pointer"):
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
            push = "@" + self.file_name + "." + str(index) + "\n" + \
                   "D=M\n" + \
                   "@SP\n" + \
                   "A=M\n" + \
                   "M=D\n" + \
                   "@SP\n" + \
                   "M=M+1\n"
        return push

    def pop1(self, segment: str, index: int):
        pop = ''
        if (segment in {"argument", "that", "this", "local"}):
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
                  "@" + self.file_name + "." + str(index) + "\n" + \
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
        #label_name = '(' + self.file_name + "$" + label + ')\n'
        label_name = '(' + self.label_func + label + ')\n'
        self.output_file.write(label_name)

    def write_init(self):
        command = "@256\n" + \
                  "D=A\n" + \
                  "@SP\n" + \
                  "M=D\n"
        self.output_file.write(command)
        self.write_call("Sys.init", 0)

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        #goto_name = '@' + self.file_name + "$" + label + "\n" + \
        #            "0;JMP\n"
        goto_name = '@' + self.label_func + label + "\n" + \
                    "0;JMP\n"
        self.output_file.write(goto_name)

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        #command_type1 = "@SP\n" + \
        #                "M=M-1\n" + \
        #                "@SP\n" + \
        #                "A=M\n" + \
        #                "D=M\n" \
        #                "@" + self.file_name + "$" + label + "\n" + \
        #                "D;JNE\n"
        command_type1 = "@SP\n" + \
                        "M=M-1\n" + \
                        "@SP\n" + \
                        "A=M\n" + \
                        "D=M\n" \
                        "@" + self.label_func + label + "\n" + \
                        "D;JNE\n"
        self.output_file.write(command_type1)

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
        # self.write_label(function_name)
        self.label_func = function_name + "$"
        func_ = '(' + function_name + ')\n'
        for i in range(int(n_vars)):
            func_ += "@0\n" + \
                     "D=A\n" + \
                     PUSH
        self.output_file.write(func_)


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
        CodeWriter.unique_counter += 1
        return_address = function_name + "$ret." + str(CodeWriter.unique_counter)
        result = "@" + return_address + '\n' + \
                 "D=A\n" + PUSH
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            result += "@" + segment + "\n" + "D=M\n" + PUSH
        result += "@SP\n" + \
                  "D=M\n" + \
                  "@" + str(int(n_args) + 5) + "\n" + \
                  "D=D-A\n" + \
                  "@ARG\n" + \
                  "M=D //ARG = SP-5-n_args\n" + \
                  "@SP\n" + \
                  "D=M\n" + \
                  "@LCL\n" + \
                  "M=D\n" + \
                  "@" + function_name + "\n" + \
                  "0;JMP\n" + \
                  "(" + return_address + ")\n"
        self.output_file.write(result)


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
        result = "@LCL\n" + \
                 "D=M\n" + \
                 "@frame\n" + \
                 "M=D // frame = LCL\n" + \
                 "@5\n" + \
                 "A=D-A\n" + \
                 "D=M\n" + \
                 "@R14\n" + \
                 "M=D // return_address = *(frame-5)\n" + \
                 "@SP\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@ARG\n" + \
                 "A=M\n" + \
                 "M=D // *ARG = pop()\n" + \
                 "@ARG\n" + \
                 "D=M+1\n" + \
                 "@SP\n" + \
                 "M=D //SP = ARG + 1\n" + \
                 "@frame\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@THAT\n" + \
                 "M=D //THAT = *(frame-1)\n" + \
                 "@frame\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@THIS\n" + \
                 "M=D // THIS = *(frame-2)\n" + \
                 "@frame\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@ARG\n" + \
                 "M=D // ARG = *(frame-3)\n" + \
                 "@frame\n" + \
                 "M=M-1\n" + \
                 "A=M\n" + \
                 "D=M\n" + \
                 "@LCL\n" + \
                 "M=D //LCL = *(frame-4)\n" + \
                 "@R14\n" + \
                 "A=M\n" + \
                 "0;JMP\n"
        self.output_file.write(result + "\n")

