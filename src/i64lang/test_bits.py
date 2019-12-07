import pytest
from . bits import Bits

def test_create_from_string():
    assert Bits("0101") == "0101"

def test_create_from_hex():
    assert Bits.from_hex("00") == "0000 0000"
    assert Bits.from_hex("0x01") == "0000 0001"
    assert Bits.from_hex("") == ""
    assert Bits.from_hex("1BF") == "0001 1011 1111"

def test_create_from_int():
    assert Bits.from_int(0, length=5) == "00000"
    assert Bits.from_int(12, length=4) == "1100"
    assert Bits.from_int(16) == "10000"
    assert Bits.from_int(-1, length=6) == "111111"
    assert Bits.from_int(-42, length=8) == "11010110"

    with pytest.raises(Exception):
        Bits.from_int(-1)

def test_create_zeros():
    assert Bits.zeros(5) == Bits("00000")

def test_create_from_hex_and_offset():
    assert Bits.from_hex_and_offset("32", 0) == "0011 0010"
    assert Bits.from_hex_and_offset("32", 1) == "0011 0011"
    assert Bits.from_hex_and_offset("32", 8) == "0011 1010"

def test_join():
    assert Bits.join(Bits("0101"), Bits("1100")) == "0101 1100"

def test_reversed_bytes():
    assert Bits.from_hex("010203").reversed_bytes().to_hex() == "030201"

def test_to_bin():
    assert Bits("0101").to_bin() == "0101"

def test_byte_len():
    assert Bits.from_hex("014523").byte_len == 3

def test_add():
    assert Bits("0101") + Bits("1100") == "0101 1100"

def test_getitem():
    bits = Bits("0101")
    assert bits[0] == "0"
    assert bits[1] == "1"
    assert bits[2] == "0"
    assert bits[3] == "1"

def test_int():
    assert int(Bits("1100")) == 12
