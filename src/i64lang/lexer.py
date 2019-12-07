__all__ = [
    "tokenize"
]

from typing import Union, List, Set, Optional
from collections import defaultdict
from string import digits, ascii_letters, whitespace
from . code_stream import CodeStream

from . tokens import (
    NameToken,
    IntToken,
    SymbolToken,
    Token
)

identifier_begins = set(ascii_letters + "_")
identifier_continuations = set(digits + ascii_letters + "_")

def tokenize_str(code: str) -> List[Token]:
    return tokenize(CodeStream(code))

def tokenize(code: CodeStream) -> List[Token]:
    tokens = list(iter_tokens(code))
    return tokens

def iter_tokens(code: CodeStream):
    while next_char := code.try_peek_next():
        if symbol_token := try_tokenize_symbol(code):
            yield symbol_token
        elif next_char in digits:
            yield tokenize_int(code)
        elif next_char in identifier_begins:
            yield tokenize_name(code)
        elif next_char in whitespace:
            code.consume_next()
        else:
            raise ValueError(f"unknown symbol: {repr(next_char)}")

possible_symbols = list("{}()+-*/=;<>,") + ["==", "!=", "<=", ">="]
symbols_by_first_char = defaultdict(list)
for symbol in possible_symbols:
    symbols_by_first_char[symbol[0]].append(symbol)

sorted_symbols_by_first_char = {first_char : tuple(sorted(symbols, key=len, reverse=True))
                                for first_char, symbols in symbols_by_first_char.items()}

def try_tokenize_symbol(code: CodeStream) -> Optional[SymbolToken]:
    first_char = code.try_peek_next()
    for symbol in sorted_symbols_by_first_char.get(first_char, ()):
        if code.next_is(symbol):
            code.skip_n(len(symbol))
            return SymbolToken(symbol)
    return None

def tokenize_int(code: CodeStream) -> IntToken:
    chars = code.consume_while(lambda c: c in digits)
    value = int(chars)
    return IntToken(value)

def tokenize_name(code: CodeStream) -> NameToken:
    identifier = code.consume_while(lambda c: c in identifier_continuations)
    return NameToken(identifier)
