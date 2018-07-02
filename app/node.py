from flask import Flask, jsonify, request
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key
        }
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        return jsonify(response), 201
    else:
        response = {
            'message': 'Saving the keys failed'
        }
        return jsonify(response), 500


@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'funds': blockchain.get_balance(),
            'public_key': wallet.public_key,
            'message': 'You have loaded your wallet successfully'
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'We could not load your keys',
            'wallet_exists?': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/balance', methods=['GET'])
def get_balance():
    if wallet.public_key != None:
        balance = blockchain.get_balance()
        response = {
            'message': 'Your balance is: {0} scoins'.format(balance)
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'We could not load your balance, please try again',
            'wallet_exists?': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/', methods=['GET'])
def get_ui():
    return 'This worked!'

@app.route('/transactions', methods=['GET'])
def open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    if open_transactions:
        response = {
            'open_transactions': dict_transactions
        }
        return jsonify(response), 200

@app.route('/transaction', methods=['POST'])
def add_transaction():
    values = request.get_json()
    required_fields = ['receiver', 'amount']
    public_key = wallet.public_key
    if public_key == None:
        response = {
          'message': 'No wallet setup'
        }
        return jsonify(response), 400
    if not values:
        response = {
            'message': 'Data not found'
        }
        return jsonify(response), 400
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Missing fields'
        }
        return jsonify(response), 400
    global blockchain
    blockchain = Blockchain(public_key)
    receiver = values['receiver']
    amount = values['amount']
    signature = wallet.sign_transaction(public_key, receiver, amount)
    if blockchain.add_transaction(receiver, public_key, signature, amount=amount):
        response = {
            'funds': blockchain.get_balance(),
            'message': 'Transaction successfull',
            'transaction': {
              'sender': public_key,
              'receiver': receiver,
              'amount': amount,
              'signature': signature
            }
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Transaction failed'
        }
        return jsonify(response), 500

@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    if block != None:
        block_dict = block.__dict__.copy()
        block_dict['transactions'] = [
            tx.__dict__ for tx in block_dict['transactions']]
        response = {
            'message': 'Block added successfully',
            'block': block_dict,
            'funds': blockchain.get_balance()
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
        block_dict['transactions'] = [
            tx.__dict__ for tx in block_dict['transactions']]
    return jsonify(chain_dict), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
