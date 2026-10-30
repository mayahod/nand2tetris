@256
D=A
@SP
M=D
@RETURN_Sys.init1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D //ARG = SP-5-n_args
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(RETURN_Sys.init1)
(Class1.set)

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

@SP
M=M-1
A=M
D=M
@Class1.0
M=D

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

@SP
M=M-1
A=M
D=M
@Class1.1
M=D

@0
D=A
@SP
A=M
M=D
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

(Class1.get)

@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1

@Class1.1
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

(Class2.set)

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

@SP
M=M-1
A=M
D=M
@Class2.0
M=D

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

@SP
M=M-1
A=M
D=M
@Class2.1
M=D

@0
D=A
@SP
A=M
M=D
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

(Class2.get)

@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1

@Class2.1
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

(Sys.init)

@6
D=A
@SP
A=M
M=D
@SP
M=M+1

@8
D=A
@SP
A=M
M=D
@SP
M=M+1

@RETURN_Class1.set1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@7
D=D-A
@ARG
M=D //ARG = SP-5-n_args
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(RETURN_Class1.set1)
@0
D=A
@5
D=A+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

@23
D=A
@SP
A=M
M=D
@SP
M=M+1

@15
D=A
@SP
A=M
M=D
@SP
M=M+1

@RETURN_Class2.set2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@7
D=D-A
@ARG
M=D //ARG = SP-5-n_args
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(RETURN_Class2.set2)
@0
D=A
@5
D=A+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D

@RETURN_Class1.get3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D //ARG = SP-5-n_args
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(RETURN_Class1.get3)
@RETURN_Class2.get4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@ARG
M=D //ARG = SP-5-n_args
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(RETURN_Class2.get4)
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP
