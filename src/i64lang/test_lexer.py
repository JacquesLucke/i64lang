import pytest

from . code_stream import CodeStream

from . lexer import (
    tokenize,
    tokenize_str,
    try_tokenize_symbol,
    tokenize_int,
    tokenize_name,
)

from . tokens import (
    NameToken,
    IntToken,
    SymbolToken,
)

class Test_tokenize:
    def test__empty_string_returns_zero_tokens(self):
        assert tokenize_str("") == []

    def test__whitespace_only_returns_zero_tokens(self):
        assert tokenize_str(" ") == []
        assert tokenize_str("    ") == []
        assert tokenize_str(" \n") == []
        assert tokenize_str(" \t") == []

    def test__multiple_identifiers(self):
        tokens = tokenize_str("ab cd ef")
        assert len(tokens) == 3
        assert tokens[0].name == "ab"
        assert tokens[1].name == "cd"
        assert tokens[2].name == "ef"

    def test__identifiers_and_integers(self):
        tokens = tokenize_str("abc 123 de45 67f")
        assert len(tokens) == 5
        assert tokens[0].name == "abc"
        assert tokens[1].value == 123
        assert tokens[2].name == "de45"
        assert tokens[3].value == 67
        assert tokens[4].name == "f"

    def test__symbols_with_whitespace(self):
        tokens = tokenize_str("+  () -\t/")
        assert len(tokens) == 5
        assert tokens[0].symbol == "+"
        assert tokens[1].symbol == "("
        assert tokens[2].symbol == ")"
        assert tokens[3].symbol == "-"
        assert tokens[4].symbol == "/"

    def test__invalid_tokens(self):
        with pytest.raises(Exception):
            tokenize_str(":")

class Test_try_tokenize_symbol:
    def test__finds_single_char(self):
        code = CodeStream("<")
        token = try_tokenize_symbol(code)
        assert token.symbol == "<"

    def test__advances_position(self):
        code = CodeStream("<a")
        token = try_tokenize_symbol(code)
        assert token.symbol == "<"
        assert code.try_peek_next() == "a"

    def test__finds_two_character_symbol(self):
        code = CodeStream("==a")
        token = try_tokenize_symbol(code)
        assert token.symbol == "=="

    def test__finds_two_and_one_character_symbol(self):
        code = CodeStream("===")
        token1 = try_tokenize_symbol(code)
        token2 = try_tokenize_symbol(code)
        assert token1.symbol == "=="
        assert token2.symbol == "="

class Test_tokenize_int:
    def test__single_digit(self):
        code = CodeStream("1a")
        token = tokenize_int(code)
        assert isinstance(token, IntToken)
        assert token.value == 1
        assert code.try_peek_next() == "a"

    def test_multiple_digits(self):
        code = CodeStream("42a")
        token = tokenize_int(code)
        assert isinstance(token, IntToken)
        assert token.value == 42
        assert code.try_peek_next() == "a"

class Test_tokenize_name:
    def test__name_only(self):
        code = CodeStream("id")
        token = tokenize_name(code)
        assert isinstance(token, NameToken)
        assert token.name == "id"
        assert code.try_peek_next() is None

    def test__multiple_names(self):
        code = CodeStream("id1 id2")
        token = tokenize_name(code)
        assert isinstance(token, NameToken)
        assert token.name == "id1"
        assert code.try_peek_next() == " "
