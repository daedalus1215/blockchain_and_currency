import datetime
import hashlib
import json
import time
from uuid import uuid4

import pytest
import requests_mock

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


def test_create_block__withProofAndPreviousHash_willReturnExpectedBlockANdResetTransaction():
    target = setup_target()
    block_id = uuid4()
    previous_hash = Blockchain.hash({
        'block_size': 1,
        'id': 122323,
        'block_header': {
            'prev_block_hash': '',
            'timestamp': time.time(),
            'target': 0000,
            'nonce': 13
        }
    })
    expected = ({
        'id': block_id,
        'block_header': {
            'nonce': 5,
            'prev_block_hash': previous_hash,
            'target': 0,
            'timestamp': str(datetime.datetime.now().isoformat(timespec='minutes')),
        },
        'block_size': 2,
        'index': 2,
        'previous_hash': previous_hash,
        'proof': 5,
        'transactions': []
    })

    actual = target.create_block(5, previous_hash, block_id)

    assert actual == expected
    assert target.transactions == []
    assert len(target.chain) == 2


def test_get_previous_block__willReturnPreviousBlock():
    target = setup_target()
    target.create_block(5, uuid4(), uuid4())
    expected = target.create_block(5, uuid4(), uuid4())

    actual = target.get_previous_block()

    assert actual == expected


def test_proof_of_work__withPreviousProof_willReturnNewProof():
    target = setup_target()

    expected = 50255

    actual = target.proof_of_work(5)

    assert actual == expected


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


def test_is_chain_valid__withInvalidPrevHash_willReturnFalse():
    target = setup_target()
    target.create_block(5, uuid4(), uuid4())
    target.create_block(5, uuid4(), uuid4())

    actual = target.is_chain_valid([{'previous_hash': 123}, {'previous_hash': 2123}, {'previous_hash': 212323}])

    assert actual is False


@pytest.fixture
def two_blocks():
    first_block = {
        "index": 1,
        "previous_hash": "0",
        "proof": 1,
        "timestamp": "2022-02-22 21:06:30.720001",
        "transactions": []
    }
    second_block = {
        "index": 2,
        "previous_hash": "7b27aae082a2f51a6f09d8dce92fc5a070f3878553643383300c9936cf0e3d4d",
        "proof": 533,
        "timestamp": "2022-02-22 21:06:48.586799",
        "transactions": [
            {
                "amount": 1,
                "from_address": "f468f44e82264b4eb3622b2df98f8616",
                "timestamp": 1645582008.586792,
                "to_address": "f468f44e82264b4eb3622b2df98f8616",
                "txid": "074b0708-2a8c-4e9c-b92e-d333ed7e0176"
            }
        ]
    }
    return [first_block, second_block]


def test_is_chain_valid__withValidPrevHash_willReturnTrue(two_blocks):
    target = setup_target()

    actual = target.is_chain_valid(two_blocks)

    assert actual is True


def test_add_node__withNodeAddress_willAddNodeToNodes():
    target = setup_target()
    expected = {'192.168.1.192'}

    target.add_node('http://192.168.1.192')

    assert target.nodes == expected


def test_replace_chain__withLongestChainInAnotherNode_willReturnTrue(two_blocks):
    with requests_mock.Mocker() as m:
        m.get('http://192.168.1.193/get_chain', json={'chain': two_blocks, 'length': 2})
        target = setup_target()
        target.add_node('http://192.168.1.193')

        actual = target.replace_chain()

        assert actual is True


def test_replace_chain__withEqualChainInAnotherNode_willReturnFalse(two_blocks):
    with requests_mock.Mocker() as m:
        m.get('http://192.168.1.192/get_chain', json={'chain': two_blocks[0], 'length': 1})
        target = setup_target()
        target.add_node('http://192.168.1.192')

        actual = target.replace_chain()

        assert actual is False
        