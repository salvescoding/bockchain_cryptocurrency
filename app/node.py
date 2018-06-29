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

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    chain_dict = [block.__dict__.copy() for block in chain_snapshot]
    for block_dict in chain_dict:
        block_dict['transactions'] = [tx.__dict__ for tx in block_dict['transactions']]
    return jsonify(chain_dict), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
