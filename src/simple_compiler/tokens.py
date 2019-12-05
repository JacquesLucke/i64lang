class Token:
    pass

class IdentifierToken(Token):
    def __init__(self, identifier: str):
        assert len(identifier) > 0
        self.identifier = identifier

    def __repr__(self):
        return f"<Identifier: {self.identifier}>"

class IntegerToken(Token):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"<Integer: {self.value}>"

class SymbolToken(Token):
    def __init__(self, symbol: str):
        assert len(symbol) > 0
        self.symbol = symbol

    def __repr__(self):
        return f"<Symbol: {self.symbol}>"
