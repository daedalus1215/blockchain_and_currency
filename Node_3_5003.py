from uuid import uuid4

from flask import Flask, jsonify, request

# Part 2 - Mining our blockchain

# Creating a web app
from Blockchain import Blockchain

app = Flask('blockchain')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

HOST = '127.0.0.1'
PORT = '5003'
blockchain = Blockchain(f"http://{HOST}:{PORT}")


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']

    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # @TODO: This would be coinbase transaction and doesnt really have a from address
    blockchain.add_transaction(node_address, node_address, 1)
    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']
                }
    return jsonify(response), 200


@app.route('/get_address', methods=['GET'])
def get_address():
    return blockchain.get_address()


# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# check if the Blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    response = {'isChainValid': blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200


# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    print(json)
    transaction_keys = ['to', 'from', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['from'], json['to'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201


# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Hadcoin Blockchain now contains the following nodes: ',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        return jsonify({'message': 'The nodes had diff chains so the chain was rep by the longest one',
                        'new_chain': blockchain.chain}), 200
    else:
        return jsonify({'message': ' All good. The chain is the largest one.', 'actual_chain': blockchain.chain}), 200


# Part 3 - Decentralizing our Blockchain
# Running the app
app.run(host=HOST, port=PORT)
