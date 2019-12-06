__all__ = [
    "tokenize"
]

from typing import Union, List

from . code_stream import CodeStream

from . tokens import (
    NameToken,
    IntToken,
    SymbolToken,
    Token
)

from string import digits, ascii_letters, whitespace

identifier_begins = set(ascii_letters + "_")
identifier_continuations = set(digits + ascii_letters + "_")

def tokenize_str(code: str) -> List[Token]:
    return tokenize(CodeStream(code))

def tokenize(code: CodeStream) -> List[Token]:
    tokens = list(iter_tokens(code))
    return tokens

def iter_tokens(code: CodeStream):
    while next_char := code.try_peek_next():
        if next_char in "{}()[]+-*/":
            yield tokenize_single_char_symbol(code)
        elif next_char in digits:
            yield tokenize_int(code)
        elif next_char in identifier_begins:
            yield tokenize_name(code)
        elif next_char in whitespace:
            code.consume_next()
        else:
            raise ValueError(f"unknown symbol: {repr(next_char)}")

def tokenize_single_char_symbol(code: CodeStream) -> SymbolToken:
    char = code.consume_next()
    return SymbolToken(char)

def tokenize_int(code: CodeStream) -> IntToken:
    chars = code.consume_while(lambda c: c in digits)
    value = int(chars)
    return IntToken(value)

def tokenize_name(code: CodeStream) -> NameToken:
    identifier = code.consume_while(lambda c: c in identifier_continuations)
    return NameToken(identifier)
