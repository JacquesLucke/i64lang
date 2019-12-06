from dataclasses import dataclass

class Token:
    pass

@dataclass
class NameToken(Token):
    name: str

@dataclass
class IntToken(Token):
    value: int

@dataclass
class SymbolToken(Token):
    symbol: str
