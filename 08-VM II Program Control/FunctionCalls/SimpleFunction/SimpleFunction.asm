(SimpleFunction.test)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// add command
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1
// not command
@SP
M=M-1
A=M
M=!M
@SP
M=M+1
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// add command
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub command
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@LCL
D=M
@R13
M=D // frame = LCL
@5
A=D-A
D=M
@R14
M=D // return_address = *(frame-5)
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D // *ARG = pop()
@ARG
D=M+1
@SP
M=D //SP = ARG + 1
@R13
M=M-1
A=M
D=M
@THAT
M=D //THAT = *(frame-1)
@R13
M=M-1
A=M
D=M
@THIS
M=D // THIS = *(frame-2)
@R13
M=M-1
A=M
D=M
@ARG
M=D // ARG = *(frame-3)
@R13
M=M-1
A=M
D=M
@LCL
M=D //LCL = *(frame-4)
@R14
A=M
0;JMP

