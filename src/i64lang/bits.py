from __future__ import annotations

class Bits:
    def __init__(self, bit_string: str):
        Bits.assert_str_is_bit_string(bit_string)
        self.bit_string = bit_string

    @staticmethod
    def assert_str_is_bit_string(text):
        assert isinstance(text, str)
        assert all(c in "01" for c in text)

    @staticmethod
    def zeros(length) -> Bits:
        return Bits("0" * length)

    @staticmethod
    def from_int(number: int, length=None):
        if length is None:
            if number >= 0:
                return Bits(bin(number)[2:])
            else:
                raise Exception("length has to be given when using negative integers")
        else:
            bit_string = int_to_bits(number, length)
            return Bits(bit_string)

    @staticmethod
    def from_hex(hex_string: str):
        if hex_string.startswith("0x"):
            hex_string = hex_string[2:]
        if len(hex_string) == 0:
            return Bits("")
        number = int(hex_string, base=16)
        length = len(hex_string) * 4
        return Bits.from_int(number, length)

    @staticmethod
    def from_hex_and_offset(hex_string: str, offset: int):
        return Bits.from_hex(hex(int(hex_string, base=16) + offset))

    @staticmethod
    def join(*args):
        return Bits("".join(b.bit_string for b in args))

    def reversed_bytes(self):
        length = len(self)
        assert length % 8 == 0
        new_bit_string = ""
        for i in range(length - 8, -1, -8):
            new_bit_string += self.bit_string[i:i + 8]
        return Bits(new_bit_string)

    def to_bin(self):
        return self.bit_string

    def to_hex(self):
        assert len(self) % 4 == 0
        return "".join(bin_to_hex_dict[bit_string] for bit_string in iter_sequence_parts(self.bit_string, 4))

    @property
    def byte_len(self):
        assert len(self) % 8 == 0
        return len(self) // 8

    def __eq__(self, other):
        if isinstance(other, str):
            return self.bit_string == other.replace(" ", "")
        elif isinstance(other, Bits):
            return self.bit_string == other.bit_string
        else:
            raise Exception("cannot compare")

    def __add__(self, other):
        return Bits(self.bit_string + other.bit_string)

    def __len__(self):
        return len(self.bit_string)

    def __getitem__(self, index_or_slice):
        return Bits(self.bit_string[index_or_slice])

    def __repr__(self):
        text = "0x" + self.to_hex() if len(self) % 4 == 0 else self.to_bin()
        return f"<Bits: {text}>"

    def __int__(self):
        return int(self.bit_string, base=2)


def int_to_bits(number: int, length: int):
    if number < 0:
        result = complement(bin(abs(number) - 1)[2:]).rjust(length, "1")
    else:
        result = bin(number)[2:].rjust(length, "0")
    if len(result) > length:
        raise Exception("number requires more bits than specified by length")
    return result

def complement(bit_string: str):
    return "".join(complement_dict[c] for c in bit_string)

def iter_sequence_parts(sequence, part_length):
    assert len(sequence) % part_length == 0
    for i in range(0, len(sequence), part_length):
        yield sequence[i:i + part_length]

complement_dict = {"0" : "1", "1" : "0"}
bin_to_hex_dict = {bin(i)[2:].zfill(4) : hex(i)[2:].upper() for i in range(16)}
