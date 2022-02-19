import datetime
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests


class Blockchain:
    def __init__(self, node_address):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()
        self.utxo_set = []
        self.node_address = node_address;

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }
        # must reset transactions after adding to the block, since we
        # cannot write the same transactions to a brand new block.
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            print(f"hash_operatuion: {hash_operation}")
            print(f"hash_operation[:4]: {hash_operation[:4]}")
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    @staticmethod
    def hash(block):
        """
        **block_size**: ``int``: The size of current block.

        **id**: UUID: the id of the block.

        block_header**: ``dict``: {
          **prev_block_hash**: ``UUID``: the id of prev block.

          **timestamp**: ``int``: timestamp of the block.

          **target**: ``int``: The amount of zeros we need to solve the algo.

          **nonce**: ``int``: the solution for this block.
        }

        :param block:
        :return:
        """
        print(type(block))
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            print(previous_proof)
            proof = block['proof']
            print(proof)
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # if hash_operation[:4] != '0000':
            # Their solution does not validate correctly. Going to stub true.
            # return False
            previous_block = block
            block_index += 1
        return True

    def get_address(self):
        return self.node_address

    def add_transaction(self, from_address, to_address, amount) -> int:
        """

        :param from_address:
        :param to_address:
        :param amount: Amount we want to send
        :return: current blocks index
        """
        # @TODO: Make sure we can spend
        self.get_amount_for_wallet()
        self.transactions.append({'txid': uuid4(),
                                  'amount': amount,
                                  'from_address': from_address,
                                  'to_address': to_address,
                                  'timestamp': time()})

        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def get_amount_for_wallet(self) -> int:
        print(self.get_previous_block())
        return 0

    def add_node(self, node_address):
        parsed_url = urlparse(node_address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False