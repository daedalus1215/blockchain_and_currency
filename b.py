#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 21:38:48 2021
"""

app = Flask(__name__)

blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work[previous_proof]
    blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message', 'Congratulations, you just mined a block!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('get_chain', methods = ['GET'])
def get_chain():
    
