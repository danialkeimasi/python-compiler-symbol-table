from pprint import pprint
from dataclasses import dataclass, field
from typing import List

from tabulate import tabulate
from typer import Typer
from sly import Lexer


app = Typer()


class Scanner(Lexer):
    """Lexer class for scanning the code.
    """
    tokens = {
        IF_KW, ELSE_KW, FOR_KW, CONST_STR, CONST_NUMBER, PLUS_OP, MINUS_OP, MULTIPLY_OP,
        DIVIDE_OP, LP, LCB, RP, RCB, EQUAL_OP, ASSIGNMENT_OP, SEMICOLON, IDENTIFIER,
    }

    ignore = ' \t\n'

    IF_KW = r'if'
    ELSE_KW = r'else'
    FOR_KW = r'for'
    CONST_STR = r'".*?"|\'.*?\''
    CONST_NUMBER = r'\d+'

    PLUS_OP = r'\+'
    MINUS_OP = r'\-'
    MULTIPLY_OP = r'\*'
    DIVIDE_OP = r'\/'
    LP = r'\('
    LCB = r'\{'
    RP = r'\)'
    RCB = r'\}'

    EQUAL_OP = r'=='
    ASSIGNMENT_OP = r'='
    SEMICOLON = r';'
    IDENTIFIER = r'[a-zA-Z_]\w*'

    variable_tokens = [
        'IDENTIFIER',
        'CONST_STR',
        'CONST_NUMBER',
    ]

    def get_tokens_symbol_table(self, data):
        """tokenize the input and gets tokens and symbol table

        Args:
            data (str): data that needs to tokenize

        Returns:
            tuple(List[Token], SymbolTable): tokens and symbol table
        """

        counter = 1
        tokens = []
        symbol_table = SymbolTable()

        for token in self.tokenize(data):
            if token.type in self.variable_tokens:
                if token_type := symbol_table.get_type_if_duplicate(token):
                    token.type = token_type
                else:
                    token.type += f'_{counter}'
                    counter += 1
                    symbol_table.add(token)

            tokens.append(token)

        return tokens, symbol_table


@dataclass
class Symbol:
    """Represents one symbol in the symbol table.
    """
    type: str
    value: str


@dataclass
class SymbolTable:
    """Contains list of symbols in the symbol table.
    """
    symbols: List[Symbol] = field(default_factory=list)

    def add(self, token):
        """add new token in to the symbol table.

        Args:
            token (Token): the Token object generated by sly.
        """
        self.symbols.append(Symbol(type=token.type, value=token.value))

    def get_type_if_duplicate(self, token):
        """gets the type of prev token if the given token
        is a duplicate IDENTIFIER.

        Args:
            token (Token): object of sly Token.

        Returns:
            str: token type if it's exist.
        """
        symbol_type = [s.type for s in self.symbols if s.value == token.value and s.type.startswith('IDENTIFIER')]
        return symbol_type[0] if symbol_type else ''

    def __str__(self):
        """this function make a table to show the symbol table in to the cli.

        Returns:
            str: symbol table as string.
        """
        return tabulate(
            [(i, s.type, s.value) for i, s in enumerate(self.symbols)],
            headers=['#', 'token type', 'value'],
            tablefmt='psql'
        )


@app.command()
def compile(file_address):
    """main function.

    Args:
        file_address (str): address of file that given in the command line.
    """

    scanner = Scanner()
    data = open(file_address, 'r').read()

    tokens, symbol_table = scanner.get_tokens_symbol_table(data)

    pprint(tokens)
    print(symbol_table)


if __name__ == '__main__':
    app()
