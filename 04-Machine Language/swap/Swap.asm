// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.

    @countermax //16
    M=0
    @countermin //17
    M=0
    @R14
    D=M
    @countertempmax //18
    M=D
    @countertempmin //19
    M=D
    @R14
    D=M
    A=D
    D=M
    @min // min=arr[0]
    M=D
    @max // max=arr[0]
    M=D

(LOOPMAX)
    @countermax
    M=M+1
    @countermax
    D=M
    @R15
    D=M-D
    @LOOPMIN
    D;JEQ
    @countermax
    D=M
    @R14
    D=M+D
    A=D
    D=M // D holds the value of the arr in counter place
    @max
    D=D-M
    @MAX
    D;JGT
    @LOOPMAX
    0;JMP

(MAX)
    @R14
    D=M
    @countermax
    D=M+D
    A=D
    D=M  // arr[countermax]
    @max
    M=D
    @R14
    D=M
    @countertempmax //18
    M=D
    @countermax
    D=M
    @countertempmax
    M=M+D
    @LOOPMAX
    0;JMP

(LOOPMIN)
    @countermin
    M=M+1
    @countermin
    D=M
    @R15
    D=M-D
    @STOP
    D;JEQ
    @countermin
    D=M
    @R14
    D=M+D
    A=D
    D=M //arr[countermin]
    @min
    D=M-D
    @MIN
    D;JGT
    @LOOPMIN
    0;JMP

(MIN)
    @R14
    D=M
    @countermin
    D=M+D
    A=D
    D=M
    @min
    M=D
    @R14
    D=M
    @countertempmin //18
    M=D
    @countermin
    D=M
    @countertempmin
    M=M+D
    @LOOPMIN
    0;JMP

(STOP)
    @min
    D=M
    @countertempmax
    A=M
    M=D // arr[countertempmax] = min

    @max
    D=M
    @countertempmin
    A=M
    M=D // arr[countertempmin] = max

(END)
    @END
    0;JMP