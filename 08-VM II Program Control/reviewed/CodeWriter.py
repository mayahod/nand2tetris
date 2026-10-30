"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import os
import typing


PUSH_D = (
    "@SP\n"
    "A=M\n"
    "M=D\n"
    "@SP\n"
    "M=M+1\n"
)

BASE_SEGMENTS = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}


class CodeWriter:
    """Translates parsed VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        self.output_file = output_stream
        self.file_name = ""
        self.current_function = ""
        self.label_counter = 0
        self.return_counter = 0

    def _write(self, assembly: str) -> None:
        self.output_file.write(assembly)

    def _next_label_id(self) -> int:
        self.label_counter += 1
        return self.label_counter

    def set_file_name(self, filename: str) -> None:
        """Set the current VM file name for static-variable symbols."""
        self.file_name = os.path.splitext(os.path.basename(filename))[0]
        self.current_function = ""

    def _binary_operation(self, operation: str) -> str:
        return (
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "A=A-1\n"
            f"M=M{operation}D\n"
        )

    def _unary_operation(self, operation: str) -> str:
        return (
            "@SP\n"
            "A=M-1\n"
            f"M={operation}M\n"
        )

    def write_arithmetic(self, command: str) -> None:
        """Translate one arithmetic/logical VM command."""
        if command == "add":
            assembly = self._binary_operation("+")
        elif command == "sub":
            assembly = self._binary_operation("-")
        elif command == "and":
            assembly = self._binary_operation("&")
        elif command == "or":
            assembly = self._binary_operation("|")
        elif command == "neg":
            assembly = self._unary_operation("-")
        elif command == "not":
            assembly = self._unary_operation("!")
        elif command == "shiftleft":
            # Hebrew University Hack extension syntax.
            assembly = self._unary_operation("<<")
        elif command == "shiftright":
            # Hebrew University Hack extension syntax.
            assembly = self._unary_operation(">>")
        elif command in {"eq", "gt", "lt"}:
            assembly = self._comparison(command)
        else:
            raise ValueError(f"Unsupported arithmetic command: {command}")

        self._write(assembly)

    def _comparison(self, command: str) -> str:
        """Generate an overflow-safe signed comparison."""
        label_id = self._next_label_id()
        true_label = f"VM_COMPARE_TRUE_{label_id}"
        false_label = f"VM_COMPARE_FALSE_{label_id}"
        same_sign_label = f"VM_COMPARE_SAME_SIGN_{label_id}"
        x_negative_label = f"VM_COMPARE_X_NEGATIVE_{label_id}"
        end_label = f"VM_COMPARE_END_{label_id}"

        # Equality can use subtraction directly: x-y is zero iff x == y,
        # regardless of signed overflow.
        if command == "eq":
            return (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "@R13\n"
                "M=D\n"
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "@R13\n"
                "D=D-M\n"
                f"@{true_label}\n"
                "D;JEQ\n"
                f"@{false_label}\n"
                "0;JMP\n"
                f"({true_label})\n"
                "D=-1\n"
                f"@{end_label}\n"
                "0;JMP\n"
                f"({false_label})\n"
                "D=0\n"
                f"({end_label})\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
            )

        jump_if_same_sign = "JGT" if command == "gt" else "JLT"
        x_nonnegative_y_negative_target = (
            true_label if command == "gt" else false_label
        )
        x_negative_y_nonnegative_target = (
            false_label if command == "gt" else true_label
        )

        return (
            # pop y -> R13
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "@R13\n"
            "M=D\n"
            # pop x -> R14
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "@R14\n"
            "M=D\n"
            # Branch according to x sign.
            f"@{x_negative_label}\n"
            "D;JLT\n"
            # x >= 0. If y < 0, result is known immediately.
            "@R13\n"
            "D=M\n"
            f"@{x_nonnegative_y_negative_target}\n"
            "D;JLT\n"
            f"@{same_sign_label}\n"
            "0;JMP\n"
            # x < 0. If y >= 0, result is known immediately.
            f"({x_negative_label})\n"
            "@R13\n"
            "D=M\n"
            f"@{x_negative_y_nonnegative_target}\n"
            "D;JGE\n"
            # Same sign: x-y cannot overflow.
            f"({same_sign_label})\n"
            "@R14\n"
            "D=M\n"
            "@R13\n"
            "D=D-M\n"
            f"@{true_label}\n"
            f"D;{jump_if_same_sign}\n"
            f"@{false_label}\n"
            "0;JMP\n"
            f"({true_label})\n"
            "D=-1\n"
            f"@{end_label}\n"
            "0;JMP\n"
            f"({false_label})\n"
            "D=0\n"
            f"({end_label})\n"
            "@SP\n"
            "A=M\n"
            "M=D\n"
            "@SP\n"
            "M=M+1\n"
        )

    def _push_from_address(self, address_code: str) -> str:
        return address_code + "D=M\n" + PUSH_D

    def _validate_index(self, segment: str, index: int) -> None:
        if index < 0:
            raise ValueError("Segment index must be non-negative.")
        if segment == "pointer" and index not in {0, 1}:
            raise ValueError("Pointer index must be 0 or 1.")
        if segment == "temp" and not 0 <= index <= 7:
            raise ValueError("Temp index must be between 0 and 7.")

    def _push(self, segment: str, index: int) -> str:
        self._validate_index(segment, index)

        if segment == "constant":
            return f"@{index}\nD=A\n" + PUSH_D

        if segment in BASE_SEGMENTS:
            base = BASE_SEGMENTS[segment]
            return (
                f"@{index}\n"
                "D=A\n"
                f"@{base}\n"
                "A=D+M\n"
                "D=M\n"
                + PUSH_D
            )

        if segment == "pointer":
            register = 3 + index
            return self._push_from_address(f"@R{register}\n")

        if segment == "temp":
            register = 5 + index
            return self._push_from_address(f"@R{register}\n")

        if segment == "static":
            return self._push_from_address(
                f"@{self.file_name}.{index}\n")

        raise ValueError(f"Unknown memory segment: {segment}")

    def _pop(self, segment: str, index: int) -> str:
        self._validate_index(segment, index)

        if segment == "constant":
            raise ValueError("Cannot pop into the constant segment.")

        if segment in BASE_SEGMENTS:
            base = BASE_SEGMENTS[segment]
            return (
                f"@{index}\n"
                "D=A\n"
                f"@{base}\n"
                "D=D+M\n"
                "@R13\n"
                "M=D\n"
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "@R13\n"
                "A=M\n"
                "M=D\n"
            )

        if segment == "pointer":
            register = 3 + index
            return (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                f"@R{register}\n"
                "M=D\n"
            )

        if segment == "temp":
            register = 5 + index
            return (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                f"@R{register}\n"
                "M=D\n"
            )

        if segment == "static":
            return (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                f"@{self.file_name}.{index}\n"
                "M=D\n"
            )

        raise ValueError(f"Unknown memory segment: {segment}")

    def write_push_pop(
            self, command: str, segment: str, index: int) -> None:
        """Translate a C_PUSH or C_POP command."""
        if command == "C_PUSH":
            self._write(self._push(segment, index))
        elif command == "C_POP":
            self._write(self._pop(segment, index))
        else:
            raise ValueError(f"Expected C_PUSH or C_POP, got: {command}")

    def _scoped_label(self, label: str) -> str:
        if self.current_function:
            return f"{self.current_function}${label}"
        return label

    def write_label(self, label: str) -> None:
        """Write a VM label in the current function scope."""
        self._write(f"({self._scoped_label(label)})\n")

    def write_goto(self, label: str) -> None:
        """Write an unconditional goto."""
        self._write(
            f"@{self._scoped_label(label)}\n"
            "0;JMP\n"
        )

    def write_if(self, label: str) -> None:
        """Pop the stack and jump when the value is non-zero."""
        self._write(
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            f"@{self._scoped_label(label)}\n"
            "D;JNE\n"
        )

    def write_init(self) -> None:
        """Write bootstrap code: SP=256 and call Sys.init."""
        self._write(
            "@256\n"
            "D=A\n"
            "@SP\n"
            "M=D\n"
        )
        self.write_call("Sys.init", 0)

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Declare a function and initialize its local variables to zero."""
        self.current_function = function_name
        self._write(f"({function_name})\n")

        for _ in range(n_vars):
            self._write("@0\nD=A\n" + PUSH_D)

    def write_call(self, function_name: str, n_args: int) -> None:
        """Write the standard Hack VM function-call sequence."""
        self.return_counter += 1
        return_label = (
            f"{self.current_function or self.file_name or 'BOOTSTRAP'}"
            f"$ret.{self.return_counter}"
        )

        self._write(f"@{return_label}\nD=A\n" + PUSH_D)

        for segment in ("LCL", "ARG", "THIS", "THAT"):
            self._write(f"@{segment}\nD=M\n" + PUSH_D)

        self._write(
            "@SP\n"
            "D=M\n"
            f"@{n_args + 5}\n"
            "D=D-A\n"
            "@ARG\n"
            "M=D\n"
            "@SP\n"
            "D=M\n"
            "@LCL\n"
            "M=D\n"
            f"@{function_name}\n"
            "0;JMP\n"
            f"({return_label})\n"
        )

    def write_return(self) -> None:
        """Write the standard Hack VM function-return sequence."""
        self._write(
            # FRAME = LCL
            "@LCL\n"
            "D=M\n"
            "@R13\n"
            "M=D\n"
            # RET = *(FRAME-5)
            "@5\n"
            "A=D-A\n"
            "D=M\n"
            "@R14\n"
            "M=D\n"
            # *ARG = pop()
            "@SP\n"
            "AM=M-1\n"
            "D=M\n"
            "@ARG\n"
            "A=M\n"
            "M=D\n"
            # SP = ARG + 1
            "@ARG\n"
            "D=M+1\n"
            "@SP\n"
            "M=D\n"
            # Restore THAT, THIS, ARG, LCL.
            "@R13\n"
            "AM=M-1\n"
            "D=M\n"
            "@THAT\n"
            "M=D\n"
            "@R13\n"
            "AM=M-1\n"
            "D=M\n"
            "@THIS\n"
            "M=D\n"
            "@R13\n"
            "AM=M-1\n"
            "D=M\n"
            "@ARG\n"
            "M=D\n"
            "@R13\n"
            "AM=M-1\n"
            "D=M\n"
            "@LCL\n"
            "M=D\n"
            # goto RET
            "@R14\n"
            "A=M\n"
            "0;JMP\n"
        )
