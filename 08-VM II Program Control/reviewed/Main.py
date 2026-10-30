"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import os
import sys
import typing

from CodeWriter import CodeWriter
from Parser import Parser


def translate_file(input_file: typing.TextIO, code_writer: CodeWriter) -> None:
    """Translate all VM commands from one input file.

    Args:
        input_file: Open .vm file.
        code_writer: Writer used for the shared output .asm file.
    """
    parser = Parser(input_file)
    code_writer.set_file_name(input_file.name)

    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()

        if command_type == "C_ARITHMETIC":
            code_writer.write_arithmetic(parser.arg1())
        elif command_type in {"C_PUSH", "C_POP"}:
            code_writer.write_push_pop(
                command_type, parser.arg1(), parser.arg2())
        elif command_type == "C_LABEL":
            code_writer.write_label(parser.arg1())
        elif command_type == "C_GOTO":
            code_writer.write_goto(parser.arg1())
        elif command_type == "C_IF":
            code_writer.write_if(parser.arg1())
        elif command_type == "C_FUNCTION":
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif command_type == "C_CALL":
            code_writer.write_call(parser.arg1(), parser.arg2())
        elif command_type == "C_RETURN":
            code_writer.write_return()


def collect_vm_files(input_path: str) -> tuple[list[str], str, bool]:
    """Resolve the VM inputs, output path, and bootstrap requirement.

    A directory is translated as one VM program and therefore receives
    bootstrap code. A single .vm file is translated without bootstrap code,
    which is useful for the standalone Project 7/8 test programs.
    """
    absolute_path = os.path.abspath(input_path)

    if os.path.isdir(absolute_path):
        vm_files = sorted(
            os.path.join(absolute_path, filename)
            for filename in os.listdir(absolute_path)
            if filename.lower().endswith(".vm")
        )
        output_path = os.path.join(
            absolute_path, os.path.basename(absolute_path) + ".asm")
        return vm_files, output_path, True

    if not absolute_path.lower().endswith(".vm"):
        raise ValueError("Input must be a .vm file or a directory.")

    output_path = os.path.splitext(absolute_path)[0] + ".asm"
    return [absolute_path], output_path, False


def translate_path(input_path: str) -> str:
    """Translate a .vm file or a directory containing .vm files.

    Returns:
        The generated .asm path.
    """
    vm_files, output_path, use_bootstrap = collect_vm_files(input_path)

    if not vm_files:
        raise ValueError("No .vm files were found.")

    with open(output_path, "w", encoding="utf-8") as output_file:
        code_writer = CodeWriter(output_file)

        if use_bootstrap:
            code_writer.write_init()

        for vm_path in vm_files:
            with open(vm_path, "r", encoding="utf-8") as input_file:
                translate_file(input_file, code_writer)

    return output_path


def main() -> None:
    """Command-line entry point."""
    if len(sys.argv) != 2:
        sys.exit("Invalid usage. Use: python Main.py <input.vm | directory>")

    try:
        translate_path(sys.argv[1])
    except (OSError, ValueError) as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
