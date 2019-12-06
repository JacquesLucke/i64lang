from typing import Optional, Set

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

    def try_peek_next_token(self) -> Optional[Token]:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def try_peek_next_token_of_type(self, TokenCls) -> Optional[Token]:
        if token := self.try_peek_next_token():
            if isinstance(token, TokenCls):
                return token
        return None

    def next_is_any_name(self) -> bool:
        return self.try_peek_next_token_of_type(NameToken) is not None

    def next_is_name(self, name: str) -> bool:
        if token := self.try_peek_next_token_of_type(NameToken):
            return token.name == name
        return False

    def next_is_any_symbol(self) -> bool:
        return self.try_peek_next_token_of_type(SymbolToken) is not None

    def next_is_symbol(self, symbol: str) -> bool:
        return self.next_is_any_symbol_of({symbol})

    def next_is_any_symbol_of(self, symbols: Set[str]) -> bool:
        if token := self.try_peek_next_token_of_type(SymbolToken):
            return token.symbol in symbols
        return False

    def next_is_int(self) -> bool:
        return self.try_peek_next_token_of_type(IntToken) is not None

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
        if token := self.try_peek_next_token_of_type(NameToken):
            self.position += 1
            return token.name
        else:
            raise RuntimeError("expected name")

    def consume_symbol(self):
        if token := self.try_peek_next_token_of_type(SymbolToken):
            self.position += 1
            return token.symbol
        else:
            raise RuntimeError("expected symbol")

    def consume_int(self):
        if token := self.try_peek_next_token_of_type(IntToken):
            self.position += 1
            return token.value
        else:
            raise RuntimeError("expected int")
