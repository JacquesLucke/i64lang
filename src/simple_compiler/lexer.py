__all__ = [
    "tokenize"
]

from typing import Union

from . code_stream import CodeStream

from . tokens import (
    IdentifierToken,
    IntegerToken,
    SymbolToken,
)

from string import digits, ascii_letters, whitespace

identifier_begins = set(ascii_letters + "_")
identifier_continuations = set(digits + ascii_letters + "_")

def tokenize(code: Union[str, CodeStream]):
    if isinstance(code, str):
        code = CodeStream(code)

    tokens = list(iter_tokens(code))
    return tokens

def iter_tokens(code: CodeStream):
    while next_char := code.try_peek_next():
        if next_char in "{}()[]+-*/":
            yield tokenize_single_char(code)
        elif next_char in digits:
            yield tokenize_integer(code)
        elif next_char in identifier_begins:
            yield tokenize_identifier(code)
        elif next_char in whitespace:
            code.consume_next()
        else:
            raise ValueError(f"unknown symbol: {repr(next_char)}")

def tokenize_single_char(code: CodeStream) -> SymbolToken:
    char = code.consume_next()
    return SymbolToken(char)

def tokenize_integer(code: CodeStream) -> IntegerToken:
    chars = code.consume_while(lambda c: c in digits)
    value = int(chars)
    return IntegerToken(value)

def tokenize_identifier(code: CodeStream) -> IdentifierToken:
    identifier = code.consume_while(lambda c: c in identifier_continuations)
    return IdentifierToken(identifier)
