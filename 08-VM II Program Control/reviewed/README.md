# Hack VM Translator — NAND2Tetris Project 8

A Python implementation of the NAND2Tetris VM-to-Hack-assembly translator.

The translator accepts either a single `.vm` file or a directory containing
multiple VM files and generates Hack assembly code. It supports the full Project
8 VM language, including program flow, functions, calls/returns, bootstrap
initialization, and the Hebrew University shift-command extension.

## Supported VM Commands

- Arithmetic: `add`, `sub`, `neg`
- Logical: `and`, `or`, `not`
- Comparisons: `eq`, `gt`, `lt`
- Shift extension: `shiftleft`, `shiftright`
- Memory access: `push`, `pop`
- Segments: `constant`, `local`, `argument`, `this`, `that`, `pointer`, `temp`, `static`
- Program flow: `label`, `goto`, `if-goto`
- Functions: `function`, `call`, `return`

## Architecture

The project keeps the original three-part structure:

- `Parser.py` — removes comments/whitespace, classifies VM commands, and exposes
  their arguments.
- `CodeWriter.py` — translates parsed commands into Hack assembly.
- `Main.py` — handles files/directories and coordinates parsing and output.

The supplied `VMtranslator` shell wrapper and `Makefile` are retained from the
course scaffold with their original attribution.

## Bootstrap Behavior

When the input path is a **directory**, the translator treats it as a complete
VM program and writes bootstrap code:

1. Sets `SP = 256`
2. Calls `Sys.init`

When the input is a **single `.vm` file**, no bootstrap code is added. This is
useful for standalone tests such as `BasicLoop.vm` and `SimpleFunction.vm`.

## Code Review / Cleanup

This repository is a cleaned version of the original assignment while keeping
the same overall design and translation strategy.

The review included:

- Removed old experimental comparison implementations and commented-out code.
- Replaced substring-based parsing with exact VM command parsing.
- Avoided repeatedly calling `command_type()` for the same command.
- Added clearer names and focused documentation.
- Added validation for pointer/temp segment bounds and invalid `pop constant`.
- Kept static variables file-scoped using symbols such as `Class1.0`.
- Kept labels function-scoped using `FunctionName$Label`.
- Reworked `gt` / `lt` generation to correctly handle signed 16-bit values
  without subtraction overflow.
- Replaced the symbolic temporary `frame` variable in `return` with the
  conventional `R13` / `R14` temporary registers.
- Made multi-file translation deterministic by sorting `.vm` filenames.
- Added explicit handling for invalid paths and empty directories.

## Running

Requires Python 3.

### Windows / VS Code terminal

For one VM file:

```text
python Main.py path\to\File.vm
```

For a directory containing a complete multi-file VM program:

```text
python Main.py path\to\ProgramDirectory
```

The generated `.asm` file is written next to the input.

Examples:

```text
python Main.py BasicLoop.vm
python Main.py FibonacciElement
```

### macOS / Linux

You can use the same Python command, or after running `make`:

```text
./VMtranslator <input path>
```

## Testing

The translator was checked against the Project 8 VM programs that accompanied
the original assignment:

- `BasicLoop`
- `FibonacciSeries`
- `SimpleFunction`
- `NestedCall`
- `FibonacciElement`
- `StaticsTest`

The final repository intentionally omits the course-provided `.tst`, `.cmp`,
`.out`, sample `.vm`, and generated `.asm` files.

## Project Structure

```text
.
├── Main.py
├── Parser.py
├── CodeWriter.py
├── VMtranslator
├── Makefile
├── .gitignore
└── README.md
```

## Technical Concepts

- Stack-machine translation
- Assembly code generation
- Memory-segment mapping
- Static-variable namespacing
- Function-scoped labels
- Bootstrap initialization
- Calling conventions and stack frames
- Recursive function calls
- Signed comparison and overflow handling
- Multi-file translation

## Academic Context

This project was developed as part of the NAND2Tetris / Computer Architecture
coursework at the Hebrew University of Jerusalem and was completed in
collaboration with another student.

The VM language specification, project test programs, launcher, Makefile, and
course scaffold were supplied as course material. The parser and code-generation
implementation were developed as part of the assignment.

## Collection note

The descriptions above came with this reviewed implementation. Its historical testing claims have not been independently reproduced as a full emulator suite during this upload. Course test fixtures are available in the parent project directory.
