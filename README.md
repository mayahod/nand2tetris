# Nand2Tetris

Building the Hack computing platform, from NAND-based logic gates to software translation tools.

## Overview

This repository collects my Nand2Tetris / Computer Architecture coursework at the Hebrew University of Jerusalem. It follows the layers of a computer system: digital logic, sequential circuits, a CPU and memory system, assembly language, a stack-based virtual machine, and Jack syntax analysis.

The collection includes assignment implementations, supplied examples and tests, and existing reviewed versions of the Project 5 hardware and Project 8 VM translator. Some later folders contain starter material; their status is described below.

## Project highlights

- **Hardware design:** HDL logic gates, adders, ALU, registers, RAM, CPU, and the complete Hack computer.
- **Assembler:** a Python two-pass translator with symbol resolution and support for course shift instructions.
- **Virtual machine translation:** stack operations, memory segments, branching, and function calling conventions, including a separately reviewed Project 8 version.
- **Syntax analysis:** a Python tokenizer and syntax-analysis engine for the Jack language, producing XML.
- **Jack examples and OS interfaces:** coursework examples, utilities, test programs, and unfinished OS scaffolding.

## Projects

| Project | Topic | Contents |
| --- | --- | --- |
| 01 | [Boolean Logic](01-Boolean%20Logic/README.md) | Logic gates, multiplexers, and demultiplexers implemented in HDL. |
| 02 | [Boolean Arithmetic](02-Boolean%20Arithmetic/README.md) | Half/full adders, a 16-bit adder, incrementer, ALU, and course shift extensions. |
| 03 | [Sequential Logic](03-Sequential%20Logic/README.md) | Bit storage, registers, the program counter, and hierarchical RAM chips. |
| 04 | [Machine Language](04-Machine%20Language/README.md) | Hack assembly programs for multiplication, screen filling, and swapping values. |
| 05 | [Computer Architecture](05-Computer%20Architecture/README.md) | Hack CPU, memory-mapped I/O, and complete computer, with extended ALU/CPU variants. |
| 06 | [Assembler](06-Assembler/README.md) | A two-pass Python assembler that resolves labels and variables and emits 16-bit Hack instructions, including shift instructions. |
| 07 | [VM I: Stack Arithmetic](07-VM%20I%20Stack%20Arithmetic/README.md) | Translation of stack arithmetic, logic, comparisons, and memory-segment access from VM commands to Hack assembly. |
| 08 | [VM II: Program Control](08-VM%20II%20Program%20Control/README.md) | An extension of the VM translator with labels, conditional branching, functions, calls, returns, and bootstrap initialization. |
| 09 | [High-Level Language](09-High-Level%20Language/README.md) | Jack language examples and supporting graphics utilities supplied with the coursework. |
| 10 | [Compiler I: Syntax Analysis](10-Compiler%20I%20Syntax%20Analysis/README.md) | A Python Jack tokenizer and recursive syntax-analysis engine that emit XML parse trees. |
| 12 | [Operating System](12-Operating%20System/README.md) | Jack OS class interfaces, pseudocode, and test programs for arrays, memory, math, strings, screen, keyboard, output, and system services. |

Project 11 (Jack-to-VM code generation) is not present in the supplied project folder. Project 12 contains unfinished OS scaffolding, and the root Project 9 `Main.jack` is a starter template. This collection therefore does not claim a completed end-to-end compiler and OS.

## How to run

Use **Python 3.10 or newer** for the Python tools. Use the **Hardware Simulator**, **CPU Emulator**, **VM Emulator**, **Jack Compiler**, and **TextComparer** from the compatible Nand2Tetris course distribution for simulation and comparisons. The simulator tools are not bundled here. Hebrew University shift extensions require the matching extended tools and chips.

Examples from the repository root:

```sh
python "06-Assembler/Main.py" "06-Assembler/add/Add.asm"
python "07-VM I Stack Arithmetic/Main.py" "07-VM I Stack Arithmetic/StackArithmetic/SimpleAdd/SimpleAdd.vm"
python "08-VM II Program Control/reviewed/Main.py" "08-VM II Program Control/FunctionCalls/FibonacciElement"
python "10-Compiler I Syntax Analysis/JackAnalyzer.py" "10-Compiler I Syntax Analysis/Square"
```

Commands generate outputs beside their input files. Work on copies when preserving reference outputs matters. Each project README explains its inputs, output format, and relevant test tools.

## Repository notes

- Project directories use numbered, descriptive names for easy navigation.
- Source code and attribution are preserved; this upload adds organization and documentation.
- Course `.tst`, `.cmp`, and XML fixtures are kept where supplied. Generated `.out` files, Python caches, IDE metadata, duplicate copy folders, and submission ZIP archives are omitted.
- Original `_org` folders remain as coursework reference material. `08-VM II Program Control/reviewed/` contains the existing reviewed VM translator.
- See [VALIDATION.md](VALIDATION.md) for the checks performed on this prepared collection.

## References and attribution

- [Nand2Tetris course](https://www.nand2tetris.org/)
- *The Elements of Computing Systems*, Noam Nisan and Shimon Schocken.
- [Attribution and course material](ATTRIBUTION.md)

Coursework was completed with collaborators as recorded in the original `AUTHORS` files. The numbered topic layout and overview style were inspired by [liorZats/Nand2Tetris](https://github.com/liorZats/Nand2Tetris); implementation files are taken from my local project folder.
