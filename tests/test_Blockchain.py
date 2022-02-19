import hashlib
import json
import time

from blockchain_and_currency.Blockchain import Blockchain


def test_get_address__willReturnAddress():
    target = setup_target()

    actual = target.get_address()

    assert actual == '192.168.1.1'


def setup_target():
    return Blockchain('192.168.1.1')


def test_add_node__withUrls_willSetNodesToTheirNetloc():
    target = setup_target()
    expected1 = '127.0.0.1:5001'
    expected2 = '127.0.0.1:5002'

    target.add_node(node_address=f'http://{expected1}')
    target.add_node(node_address=f'http://{expected2}')

    assert target.nodes == {expected2, expected1}


def test_hash__withBlock_willReturnHashedBlock():
    block = {
        'block_size': 1,
        'id': 122323,
        'block_header': {
            'prev_block_hash': '',
            'timestamp': time.time(),
            'target': 0000,
            'nonce': 13
        }
    }
    encoded_block = json.dumps(block, sort_keys=True).encode()
    expected = hashlib.sha256(encoded_block).hexdigest()

    actual = Blockchain.hash(block)

    assert actual == expected
