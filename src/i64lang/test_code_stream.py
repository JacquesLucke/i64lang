from . code_stream import CodeStream

class Test_CodeStream_try_peek_next:
    def test__none_when_stream_is_empty(self):
        code = CodeStream("")
        assert code.try_peek_next() is None

    def test__none_when_stream_is_at_end(self):
        code = CodeStream("abc")
        code.consume_next()
        code.consume_next()
        code.consume_next()
        assert code.try_peek_next() is None

    def test__correct_char_when_position_is_in_middle(self):
        code = CodeStream("abc")
        assert code.try_peek_next() == "a"
        code.consume_next()
        assert code.try_peek_next() == "b"
        code.consume_next()
        assert code.try_peek_next() == "c"

class Test_CodeStream_consume_next:
    def test__returns_next_char_and_increments_position(self):
        code = CodeStream("abc")
        assert code.consume_next() == "a"
        assert code.consume_next() == "b"
        assert code.consume_next() == "c"

class Test_CodeStream_consume_while:
    def test__can_return_empty_string(self):
        code = CodeStream("abc")
        assert code.consume_while(lambda c: False) == ""

    def test__can_return_partial_string(self):
        code = CodeStream("abc")
        assert code.consume_while(lambda c: c in "ba") == "ab"

    def test__can_return_entire_string(self):
        code = CodeStream("abc")
        assert code.consume_while(lambda c: True) == "abc"

    def test__returns_empty_string_on_empty_code(self):
        code = CodeStream("")
        assert code.consume_while(lambda c: True) == ""
