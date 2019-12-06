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

    def consume_expected_name(self, name: str):
        assert self.next_is_name(name)
        self.position += 1

    def consume_expected_symbol(self, symbol: str):
        assert self.next_is_symbol(symbol)
        self.position += 1

    def consume_name_or_raise(self):
        if self.position >= len(self.tokens):
            raise RuntimeError("unexpected end of tokens")

        token = self.tokens[self.position]
        if not isinstance(token, NameToken):
            raise RuntimeError(f"expected a name token but got {token}")

        self.position += 1

        return token.name

    def consume_expected_symbol_or_raise(self, symbol: str):
        self.position >= len(self.tokens):
            raise RuntimeError("unexpected end of tokens")

        token = self.tokens[self.position]
        if not isinstance(token, SymbolToken) or token.symbol != symbol:
            raise RuntimeError(f"expected a {symbol} symbol but got {token}")

        self.position += 1
