from blockchain_and_currency.helpers import encode_varint


def test__encode_varint__with1_shouldReturnSomething():
    actual = encode_varint(1)
    assert actual == 2