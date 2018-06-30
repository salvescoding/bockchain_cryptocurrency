from flask import Flask, jsonify
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)

@app.route('/', methods=['GET'])
def get_ui():
    return 'This worked!'

@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    if block != None:
        block_dict = block.__dict__.copy()
        block_dict['transactions'] = [tx.__dict__ for tx in block_dict['transactions']]
        response = {
          'message': 'Block added successfully',
          'block': block_dict
        }
        return jsonify(response), 201
    else:
        response = {
          'message': 'Adding a new block failed',
          'wallet_exists': wallet.public_key != None
        }
        return jsonify(response), 500

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    chain_dict = [block.__dict__.copy() for block in chain_snapshot]
    for block_dict in chain_dict:
        block_dict['transactions'] = [tx.__dict__ for tx in block_dict['transactions']]
    return jsonify(chain_dict), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
