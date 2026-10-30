"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.string_const_dic = {"<": "&lt;", ">": "&gt;", '"': "&qout;", "&": "&amp;"}
        self.counter_space = 0
        self.counter_row = 0

    def write_token(self, token):
        return "  " * self.counter_space + token + "\n"

    def return_token(self):
        self.input_stream.advance()
        list_token = []
        if (self.input_stream.current_token == None):
            return None
        current_token_type = self.input_stream.token_type()
        if(current_token_type == "KEYWORD"):
            list_token = ["keyword", self.input_stream.keyword()]
        elif (current_token_type == "SYMBOL"):
            list_token = ["symbol", self.input_stream.symbol()]
        elif (current_token_type == "INT_CONST"):
            list_token = ["integerConstant", self.input_stream.int_val()]
        elif (current_token_type == "IDENTIFIER"):
            list_token = ["identifier", self.input_stream.identifier()]
        elif (current_token_type == "STRING_CONST"):
            list_token = ["stringConstant", self.input_stream.string_val()]
        if(list_token[1] in self.string_const_dic):
            list_token[1] = self.string_const_dic[list_token[1]]
        if (current_token_type == "STRING_CONST"):
            for symbol, replacement in self.string_const_dic.items():
                list_token[1] = list_token[1].replace(symbol, replacement)
        return list_token

    def token_ahead_type(self):
        type, token = self.return_token()
        result = self.write_token("<%s> %s </%s>" % (type, token, type))
    #    result += self.write_token("%s" %token)
    #    result += self.write_token("</%s>" %type)
        return result

    def peek_next_token(self):
        if self.input_stream.has_more_tokens():
            token = self.input_stream.peek()
            type = self.input_stream.token_type(token)
            if type == "STRING_CONST":
                token = token[1:-1]
        else:
            token = None
            type = None
        return (token, type)


    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<class>"))
        self.counter_space +=1
        self.output_stream.write(self.token_ahead_type())
        self.output_stream.write(self.token_ahead_type())
        self.output_stream.write(self.token_ahead_type())
        while (self.peek_next_token()[0] in {"static", "field"}):
            self.compile_class_var_dec()
        while (self.peek_next_token()[0] in {"constructor", "function", "method"}):
            self.compile_subroutine()
        self.output_stream.write(self.token_ahead_type())
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</class>"))


    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<classVarDec>"))
        self.counter_space += 1
        self.output_stream.write(self.token_ahead_type())
        self.output_stream.write(self.token_ahead_type())
        self.output_stream.write(self.token_ahead_type())
        while (self.peek_next_token()[0] == ","):
            self.output_stream.write(self.token_ahead_type())
            self.output_stream.write(self.token_ahead_type())
        self.output_stream.write(self.token_ahead_type())
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</classVarDec>"))

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.output_stream.write(self.write_token("<subroutineDec>"))
        self.counter_space += 1
        self.output_stream.write(self.token_ahead_type()) #method
        self.output_stream.write(self.token_ahead_type()) #type
        self.output_stream.write(self.token_ahead_type()) #getx
        self.output_stream.write(self.token_ahead_type()) #(
        self.compile_parameter_list()
        self.output_stream.write(self.token_ahead_type()) #)
        self.output_stream.write(self.write_token("<subroutineBody>"))
        self.counter_space +=1
        self.output_stream.write(self.token_ahead_type())
        while (self.peek_next_token()[0] == "var"):
            self.compile_var_dec()
        self.compile_statements()
        self.output_stream.write(self.token_ahead_type()) #}
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</subroutineBody>"))
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</subroutineDec>"))


    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.output_stream.write(self.write_token("<parameterList>"))
        self.counter_space += 1
        while (not self.peek_next_token()[1] == "SYMBOL"):
                self.output_stream.write(self.token_ahead_type()) #type
                self.output_stream.write(self.token_ahead_type()) #name
                if (self.peek_next_token()[0] == ","):
                    self.output_stream.write(self.token_ahead_type()) #,
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</parameterList>"))


    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<varDec>"))
        self.counter_space += 1
        self.output_stream.write(self.token_ahead_type())  # var
        self.output_stream.write(self.token_ahead_type()) #type
        self.output_stream.write(self.token_ahead_type())  # name
        while (self.peek_next_token()[0] == ","):
            self.output_stream.write(self.token_ahead_type()) # ,
            self.output_stream.write(self.token_ahead_type()) #name
        self.output_stream.write(self.token_ahead_type()) #;
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</varDec>"))

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        self.output_stream.write(self.write_token("<statements>"))
        self.counter_space += 1
        token = self.peek_next_token()[0]
        while (token in {"if", "while", "let", "do", "return"}):
            if (self.peek_next_token()[0] == "if"):
                self.compile_if()
            elif (self.peek_next_token()[0] == "while"):
                self.compile_while()
            elif (self.peek_next_token()[0] == "let"):
                self.compile_let()
            elif (self.peek_next_token()[0] == "do"):
                self.compile_do()
            elif (self.peek_next_token()[0] == "return"):
                self.compile_return()
            token = self.peek_next_token()[0]
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</statements>"))

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<doStatement>"))
        self.counter_space += 1
        self.output_stream.write(self.token_ahead_type())
        self.output_stream.write(self.token_ahead_type())
        if (self.peek_next_token()[0] == "."):
            self.output_stream.write(self.token_ahead_type()) #.
            self.output_stream.write(self.token_ahead_type()) # name
        self.output_stream.write(self.token_ahead_type()) #(
        self.compile_expression_list()
        self.output_stream.write(self.token_ahead_type())  # )
        self.output_stream.write(self.token_ahead_type())  # ;
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</doStatement>"))


    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<letStatement>"))
        self.counter_space += 1
        self.output_stream.write(self.token_ahead_type()) #let
        self.output_stream.write(self.token_ahead_type()) # varname
        if(self.peek_next_token()[0] == "["):
            self.output_stream.write(self.token_ahead_type()) #[
            self.compile_expression()
            self.output_stream.write(self.token_ahead_type())#]
        self.output_stream.write(self.token_ahead_type()) #=
        self.compile_expression()
        self.output_stream.write(self.token_ahead_type()) #;
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</letStatement>"))

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<whileStatement>"))
        self.counter_space += 1
        self.output_stream.write(self.token_ahead_type()) #while
        self.output_stream.write(self.token_ahead_type()) #(
        self.compile_expression()
        self.output_stream.write(self.token_ahead_type())  # )
        self.output_stream.write(self.token_ahead_type())  # {
        self.compile_statements()
        self.output_stream.write(self.token_ahead_type())  # }
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</whileStatement>"))

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<returnStatement>"))
        self.counter_space += 1
        self.output_stream.write(self.token_ahead_type()) #return
        if (not self.peek_next_token()[0] == ";"):
            self.compile_expression()
        self.output_stream.write(self.token_ahead_type()) #;
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</returnStatement>"))


    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<ifStatement>"))
        self.counter_space += 1
        self.output_stream.write(self.token_ahead_type()) #if
        self.output_stream.write(self.token_ahead_type()) #(
        self.compile_expression()
        self.output_stream.write(self.token_ahead_type())  # )
        self.output_stream.write(self.token_ahead_type())  # (
        self.compile_statements()
        self.output_stream.write(self.token_ahead_type())  # (
        if (self.peek_next_token()[0] == "else"):
            self.output_stream.write(self.token_ahead_type())  # else
            self.output_stream.write(self.token_ahead_type())  # (
            self.compile_statements()
            self.output_stream.write(self.token_ahead_type())  # (
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</ifStatement>"))


    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<expression>"))
        self.counter_space += 1
        self.compile_term()
        while(self.peek_next_token()[0] in {"+", "-", "*", "/", "&", "|", "<", ">", "="}):
            self.output_stream.write(self.token_ahead_type())
            self.compile_term()
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</expression>"))


    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        self.output_stream.write(self.write_token("<term>"))
        self.counter_space += 1
        if(self.peek_next_token()[1] == "IDENTIFIER"):
            self.output_stream.write(self.token_ahead_type())
            if(self.peek_next_token()[0] == "["):
                self.output_stream.write(self.token_ahead_type()) #[
                self.compile_expression()
                self.output_stream.write(self.token_ahead_type()) #]
            elif(self.peek_next_token()[0] == "("):
                self.output_stream.write(self.token_ahead_type())  # (
                self.compile_expression_list()
                self.output_stream.write(self.token_ahead_type())  # )
            elif(self.peek_next_token()[0] == "."):
                self.output_stream.write(self.token_ahead_type()) #.
                self.output_stream.write(self.token_ahead_type())
                self.output_stream.write(self.token_ahead_type())
                self.compile_expression_list()
                self.output_stream.write(self.token_ahead_type())
                # result += self.token_ahead_type()
                # result += self.compile_subroutine()
        elif(self.peek_next_token()[1] in {"INT_CONST", "STRING_CONST", "KEYWORD"}):
            self.output_stream.write(self.token_ahead_type())
        elif(self.peek_next_token()[0] in {'-', '~'}):
            self.output_stream.write(self.token_ahead_type())
            self.compile_term()
        elif(self.peek_next_token()[1] == "SYMBOL"):
            self.output_stream.write(self.token_ahead_type())
            self.compile_expression()
            self.output_stream.write(self.token_ahead_type())
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</term>"))

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<expressionList>"))
        self.counter_space += 1
        if (not self.peek_next_token()[0] == ")"):
            self.compile_expression()
        while (self.peek_next_token()[0] == ","):
                self.output_stream.write(self.token_ahead_type())  # (
                self.compile_expression()
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</expressionList>"))


    def compile_expression_list1(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.output_stream.write(self.write_token("<expressionList>"))
        self.counter_space += 1
        if (self.peek_next_token()[0] == "("):
            self.output_stream.write(self.token_ahead_type()) #(
            self.compile_expression()
            while (self.peek_next_token()[0] == "("):
                self.output_stream.write(self.token_ahead_type())  # (
                self.output_stream.write(self.token_ahead_type()) #,
                self.compile_expression()
                self.output_stream.write(self.token_ahead_type())  # )
            self.output_stream.write(self.token_ahead_type())  # )
        self.counter_space -= 1
        self.output_stream.write(self.write_token("</expressionList>"))


