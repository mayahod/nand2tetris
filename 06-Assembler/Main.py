# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    parser = Parser(input_file)
    table = SymbolTable()
    current_address = 0
    #First pass
    while(parser.has_more_commands()):
        parser.advance()
        if((parser.command_type() == "A_COMMAND") or (parser.command_type() == "C_COMMAND")):
            current_address+=1
        elif(parser.command_type() == "L_COMMAND"):
            table.add_entry(parser.symbol(),current_address)
    #Second pass
    input_file.seek(0)
    parser = Parser(input_file)
    n = 16
    while(parser.has_more_commands()):
        parser.advance()
        if parser.command_type() == "A_COMMAND":
            symbol = parser.symbol()

            if symbol.isdigit():  # If it's a numeric constant
                address = int(symbol)
            elif table.contains(symbol):
                address = table.get_address(symbol)
            else:
                table.add_entry(symbol, n)
                address = n
                n += 1

            binary_symbol = format(address, '016b')
            output_file.write(binary_symbol + '\n')

        #if((parser.command_type() == "A_COMMAND")):
        #    if (table.contains(parser.symbol())):
        #        address_symbol = table.get_address(parser.symbol())
        #        binary_symbol = format(address_symbol, '016b')
        #        output_file.write(binary_symbol + '\n')
        #    else:
        #        table.add_entry(parser.symbol(), n)
        #        n+=1
        if((parser.command_type() == "C_COMMAND")):
            dest_cur = parser.dest()
            comp_cur = parser.comp()
            jump_cur = parser.jump()
            bin_dest = Code.dest(dest_cur)
            bin_comp = Code.comp(comp_cur)
            bin_jump = Code.jump(jump_cur)
            new_command = Code.instruction_c(bin_dest, bin_comp, bin_jump)
            output_file.write(new_command + '\n')




if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)