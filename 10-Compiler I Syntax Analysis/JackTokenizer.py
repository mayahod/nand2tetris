"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re

SYMBOLS = r'[\{\}\(\)\[\]\.,;\+\-\*\/\&\|\<\>\=\~]'
STRING_CONST = r'(?:\"[^\"\n]*[\"])|(?:\'[^\'\n]*[\'])'
ALL = r'(' + SYMBOLS + '|' + STRING_CONST + '|[\w]+)'
IDENTIFIER = r'[A-Za-z_]+[A-Za-z0-9_]*'
INT_CONST = r'\d+'


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_stream.read().splitlines()
        self.all_lines = input_stream.read()
        self.all_lines = self.remove_comments()
        self.input_lines = self.all_lines.splitlines()
        self.current_line = 0
        self.current_token = None
        self.input_lines = self.create_list_token()

    def create_list_token(self):
        self.input_stream1 = []
        for line in self.input_lines:
            words = re.split(ALL, line)
            words = [word.strip() for word in words]
            not_spaces = [word for word in words if word not in [" ", ""]]
            self.input_stream1.extend((not_spaces))
        return self.input_stream1

    def remove_comments(self) -> str:
        """Removes comments from a line."""
        # single-line comments
        current_index = 0
        no_comments_text = ''
        last_index = 0
        while current_index < len(self.all_lines):
            current_char = self.all_lines[current_index]
            if current_char == "/":
                if self.all_lines[current_index + 1] == "/":
                    last_index = self.all_lines.find("\n", current_index + 1)
                    current_index = last_index + 1
                    no_comments_text += " "
                elif self.all_lines[current_index + 1] == "*":
                    last_index = self.all_lines.find("*/", current_index + 1)
                    current_index = last_index + 2
                    no_comments_text += " "
                else:
                    no_comments_text += self.all_lines[current_index]
                    current_index += 1
            elif current_char == "\"":
                last_index = self.all_lines.find("\"", current_index + 1)
                no_comments_text += self.all_lines[current_index:last_index + 1]
                current_index = last_index + 1
            else:
                no_comments_text += self.all_lines[current_index]
                current_index += 1
        return no_comments_text


    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        length = len(self.input_lines)
        return (self.current_line < len(self.input_lines))

    def peek(self) -> str:
        """Returns the next token without advancing the internal pointer."""
        if self.has_more_tokens():
            return self.input_lines[self.current_line]
        else:
            return ""

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        # Your code goes here!
        if (self.has_more_tokens()):
            self.current_token = self.input_lines[self.current_line]
            self.current_line += 1

    keyword_type = {'class', 'constructor', 'function', 'method', 'field',
                    'static', 'var', 'int', 'char', 'boolean', 'void', 'true',
                    'false', 'null', 'this', 'let', 'do', 'if', 'else',
                    'while', 'return'}

    symbol_type = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
                   '-', '*', '/', '&', '|', '<', '>', '=', '~', '^', '#'}

    def token_type(self, token=None) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        # Your code goes here!
        if(self.current_token == None):
            return self.current_token
        if(token == None):
            token = self.current_token
        if(token in self.keyword_type):
            return "KEYWORD"
        elif(token in self.symbol_type):
            return "SYMBOL"
        # elif(re.match(INT_CONST,token)):
        elif (token.isdigit()):
            return "INT_CONST"
        elif ((token.startswith('"')) and (token.endswith('"'))):
            return "STRING_CONST"
        elif(re.match(IDENTIFIER,token)):
        #elif (token.isidentifier()):
            return "IDENTIFIER"



    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        if (self.token_type(self.current_token) == "KEYWORD"):
            return self.current_token
        return "not_keyword"


    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        # Your code goes here!
        if(self.token_type(self.current_token) == "SYMBOL"):
            return self.current_token
        return "not_symbol"

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        # Your code goes here!
        if (self.token_type(self.current_token) == "IDENTIFIER"):
            return self.current_token
        return "not_identifier"

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        # Your code goes here!
        if (self.token_type(self.current_token) == "INT_CONST"):
            return int(self.current_token)


    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # Your code goes here!
        if (self.token_type(self.current_token) == "STRING_CONST"):
            return self.current_token.strip('"')
        return "not_string"