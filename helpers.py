import hashlib


def hash256(s):
    """two rounds of sha256"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def encode_varint(i):
    """encodes an integer as a varint"""
    if i < 0xfd:
        return bytes([i])
    elif i < 0x1000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise ValueError('integer too large: {}'.format(i))


def little_endian_to_int(b) -> int:
    """takes byte sequence as a little-endian number."""
    return int.from_bytes(b, 'little')


def int_to_little_endian(n, length):
    """takes an integer, returns an little-endian-byte sequence of length"""
    return n.to_bytes(length, 'little')