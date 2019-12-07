from typing import Optional, Callable

class CodeStream:
    def __init__(self, code: str):
        self.code = code
        self.position = 0

    def try_peek_next(self) -> Optional[str]:
        if self.position < len(self.code):
            return self.code[self.position]
        else:
            return None

    def next_is(self, text: str):
        if self.position + len(text) <= len(self.code):
            actual_code = self.code[self.position:self.position + len(text)]
            return text == actual_code
        else:
            return False

    def skip_n(self, n: int):
        self.position += n
        assert self.position <= len(self.code)

    def consume_next(self) -> str:
        assert self.position < len(self.code)

        char = self.code[self.position]
        self.position += 1
        return char

    def consume_while(self, predicate: Callable[[str], bool]):
        consumed_chars = ""

        while next_char := self.try_peek_next():
            if predicate(next_char):
                consumed_chars += next_char
                self.consume_next()
            else:
                break

        return consumed_chars
