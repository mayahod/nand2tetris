# Hack Computer — NAND2Tetris Project 5

An HDL implementation of the Hack computer hardware platform from the
NAND2Tetris course.

The project combines the CPU, data memory, instruction ROM, and program
counter into a complete computer capable of executing Hack machine code.
It also includes the Hebrew University course extension that adds shift
operations through `ExtendAlu` and `CpuMul`.

## Implemented Chips

- `CPU.hdl` — standard Hack CPU with A/D registers, ALU control, destinations,
  jump logic, and program counter control.
- `Memory.hdl` — Hack memory map combining RAM16K, Screen, and Keyboard.
- `Computer.hdl` — top-level computer connecting ROM32K, CPU, and Memory.
- `ExtendAlu.hdl` — course extension adding left/right shift operations.
- `CpuMul.hdl` — extended CPU using `ExtendAlu`.

## Architecture

### CPU

The CPU distinguishes between A- and C-instructions using the most significant
instruction bit.

For C-instructions it:

1. Selects A or M as the ALU's second operand.
2. Evaluates the ALU control bits.
3. Loads A, D, and/or M according to the destination bits.
4. Evaluates the jump bits against the ALU's `zr` and `ng` flags.
5. Loads or increments the program counter.

### Memory

The data-memory address space is decoded as:

```text
0x0000 - 0x3FFF   RAM16K
0x4000 - 0x5FFF   Screen
0x6000            Keyboard
```

The keyboard region is treated as read-only. Writes are routed only to RAM or
Screen.

### Complete Computer

`Computer.hdl` wires:

```text
ROM32K -> CPU -> Memory
           ^       |
           |_______|
```

The CPU's `pc` selects the next ROM instruction, while `addressM`, `outM`, and
`writeM` control the data-memory access.

## Extended ALU / CPU

The Hebrew University version of the assignment also includes an extension to
the standard Hack platform.

`ExtendAlu` supports the regular ALU operations and additional left/right shift
operations. `CpuMul` integrates this extended ALU while preserving the standard
Hack destination and jump behavior.

The specification comments and attribution for this extension are preserved in
the source files.

## Code Review / Cleanup

This repository is a cleaned portfolio version of the original assignment.
The architecture and solution remain the same, while the implementation was
reviewed for readability and correctness.

Changes include:

- Replaced unclear internal wire names with descriptive names.
- Removed commented-out experimental code and submission scaffolding.
- Simplified jump-condition wiring without changing its behavior.
- Added focused comments around instruction decoding and data flow.
- Corrected memory write decoding so writes to the Keyboard / invalid address
  range are not accidentally routed to Screen.
- Kept the original external chip interfaces unchanged so the course test
  scripts remain compatible.

## Running and Testing

The project is designed for the official NAND2Tetris **Hardware Simulator**.

The clean repository intentionally does not include course-provided test files,
generated `.out` files, IDE metadata, or the NAND2Tetris tools.

### Easiest local test workflow

1. Download/extract the official NAND2Tetris software package.
2. Make a **copy** of the original `projects/05` directory.
3. Copy these five cleaned `.hdl` files into that copied directory, replacing
   the corresponding `.hdl` files:
   - `CPU.hdl`
   - `Memory.hdl`
   - `Computer.hdl`
   - `ExtendAlu.hdl`
   - `CpuMul.hdl`
4. Open the Hardware Simulator.
5. Load the appropriate `.tst` file from the copied Project 5 folder.
6. Run the script.

For example, from a Windows command prompt with the NAND2Tetris `tools`
directory available on `PATH`:

```text
HardwareSimulator CPU.tst
HardwareSimulator Memory.tst
HardwareSimulator ExtendAlu.tst
HardwareSimulator CpuMul.tst
HardwareSimulator ComputerAdd.tst
HardwareSimulator ComputerMax.tst
HardwareSimulator ComputerRect.tst
```

A successful script ends with a message such as:

```text
End of script - Comparison ended successfully
```

`Memory.tst` contains an interactive keyboard/screen portion, so it is usually
more convenient to run that test in the graphical Hardware Simulator.

## Repository Structure

```text
.
├── CPU.hdl
├── Memory.hdl
├── Computer.hdl
├── ExtendAlu.hdl
├── CpuMul.hdl
├── .gitignore
└── README.md
```

## Technical Concepts

- Combinational and sequential logic
- CPU datapath and control
- Instruction decoding
- ALU flags and conditional jumps
- Registers and program counters
- Memory-mapped I/O
- Address decoding
- Computer architecture
- Hardware Description Language (HDL)

## Academic Context

This project was developed as part of the NAND2Tetris / Computer Architecture
coursework at the Hebrew University of Jerusalem and was completed in
collaboration with another student.

The Hack platform specification, chip interfaces, course test infrastructure,
and the extended-ALU specification were provided as course material. The HDL
implementations in this repository were developed as part of the assignment.
