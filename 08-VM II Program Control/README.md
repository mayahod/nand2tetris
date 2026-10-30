# Project 08 — VM II: Program Control

An extension of the VM translator with labels, conditional branching, functions, calls, returns, and bootstrap initialization.

## Tools

Python 3 and CPU Emulator. Use the compatible course distribution for Hebrew University extensions.

## How to run

Use the reviewed implementation for new runs:

```sh
python "08-VM II Program Control/reviewed/Main.py" "08-VM II Program Control/ProgramFlow/BasicLoop/BasicLoop.vm"
python "08-VM II Program Control/reviewed/Main.py" "08-VM II Program Control/FunctionCalls/FibonacciElement"
```

A single file is translated without bootstrap. A directory is treated as a complete program and initializes SP to 256 before calling `Sys.init`. The original assignment implementation remains in this folder; it emits bootstrap code for both file and directory inputs. See `reviewed/README.md` for implementation details.

## Academic context

Part of the Nand2Tetris coursework collection. Original source notices and supplied test material are retained. See the repository [overview](../README.md) and [attribution](../ATTRIBUTION.md).
