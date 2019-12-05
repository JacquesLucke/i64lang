from . code_stream import CodeStream

from . lexer import (
    tokenize,
    tokenize_single_char,
    tokenize_integer,
    tokenize_identifier,
)

from . tokens import (
    IdentifierToken,
    IntegerToken,
    SymbolToken,
)

class Test_tokenize:
    def test__empty_string_returns_zero_tokens(self):
        assert tokenize("") == []

    def test__whitespace_only_returns_zero_tokens(self):
        assert tokenize(" ") == []
        assert tokenize("    ") == []
        assert tokenize(" \n") == []
        assert tokenize(" \t") == []

    def test__multiple_identifiers(self):
        tokens = tokenize("ab cd ef")
        assert len(tokens) == 3
        assert tokens[0].identifier == "ab"
        assert tokens[1].identifier == "cd"
        assert tokens[2].identifier == "ef"

    def test__identifiers_and_integers(self):
        tokens = tokenize("abc 123 de45 67f")
        assert len(tokens) == 5
        assert tokens[0].identifier == "abc"
        assert tokens[1].value == 123
        assert tokens[2].identifier == "de45"
        assert tokens[3].value == 67
        assert tokens[4].identifier == "f"

    def test__symbols_with_whitespace(self):
        tokens = tokenize("+  () -\t/")
        assert len(tokens) == 5
        assert tokens[0].symbol == "+"
        assert tokens[1].symbol == "("
        assert tokens[2].symbol == ")"
        assert tokens[3].symbol == "-"
        assert tokens[4].symbol == "/"

class Test_tokenize_single_char:
    def test__consumes_next_char(self):
        code = CodeStream("abc")
        token = tokenize_single_char(code)
        assert isinstance(token, SymbolToken)
        assert token.symbol == "a"
        assert code.try_peek_next() == "b"

class Test_tokenize_integer:
    def test__single_digit(self):
        code = CodeStream("1a")
        token = tokenize_integer(code)
        assert isinstance(token, IntegerToken)
        assert token.value == 1
        assert code.try_peek_next() == "a"

    def test_multiple_digits(self):
        code = CodeStream("42a")
        token = tokenize_integer(code)
        assert isinstance(token, IntegerToken)
        assert token.value == 42
        assert code.try_peek_next() == "a"

class Test_tokenize_identifier:
    def test__identifier_only(self):
        code = CodeStream("id")
        token = tokenize_identifier(code)
        assert isinstance(token, IdentifierToken)
        assert token.identifier == "id"
        assert code.try_peek_next() is None

    def test__multiple_identifiers(self):
        code = CodeStream("id1 id2")
        token = tokenize_identifier(code)
        assert isinstance(token, IdentifierToken)
        assert token.identifier == "id1"
        assert code.try_peek_next() == " "
