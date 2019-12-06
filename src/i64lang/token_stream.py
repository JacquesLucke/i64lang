from typing import Optional

from . tokens import (
    NameToken,
    IntToken,
    SymbolToken,
    Token
)

class TokenStream:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    def next_is_any_name(self) -> bool:
        if self.position < len(self.tokens):
            next_token = self.tokens[self.position]
            return isinstance(next_token, NameToken)
        return False

    def next_is_name(self, name: str) -> bool:
        if self.position < len(self.tokens):
            next_token = self.tokens[self.position]
            if isinstance(next_token, NameToken):
                return next_token.name == name
        return False

    def next_is_symbol(self, symbol: str) -> bool:
        if self.position < len(self.tokens):
            next_token = self.tokens[self.position]
            if isinstance(next_token, SymbolToken):
                return next_token.symbol == symbol
        return False

    def skip_name(self, name: str):
        if self.next_is_name(name):
            self.position += 1
        else:
            raise RuntimeError(f"expected {name}")

    def skip_symbol(self, symbol: str):
        if self.next_is_symbol(symbol):
            self.position += 1
        else:
            raise RuntimeError(f"expected {name}")

    def consume_name(self):
        if self.next_is_any_name():
            token = self.tokens[self.position]
            self.position += 1
            return token.name
        else:
            raise RuntimeError("expected name")
