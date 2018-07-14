from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain
from helpers.converter_to_dict import ConverterToDict

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')


@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'funds': blockchain.get_balance(),
            'public_key': wallet.public_key,
            'private_key': wallet.private_key
        }
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
        blockchain = Blockchain(wallet.public_key, port)
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


@app.route('/transactions', methods=['GET'])
def open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = ConverterToDict.transactions_to_dict(transactions)
    if transactions:
        response = {
            'open_transactions': dict_transactions
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'No open transactions'
        }
        return jsonify(response), 200


@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {'message': 'No data attached'}
        return jsonify(response), 400
    required = ['sender', 'receiver', 'amount', 'signature']
    if not all(key in values for key in required):
        response = {'message': 'Missing data'}
        return jsonify(response), 400
    success = blockchain.add_transaction(
        values['receiver'], values['sender'], values['signature'], values['amount'], is_receiving=True)
    if success:
        response = {
            'message': 'Transaction successfull',
            'transaction': {
                'sender': values['sender'],
                'recipient': values['receiver'],
                'amount': values['amount'],
                'signature': values["signature"]
            }
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Transaction failed'
        }
        return jsonify(response), 500


@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {'message': 'No data attached'}
        return jsonify(response), 400
    if not 'block' in values:
        response = {'message': 'No block added'}
        return jsonify(response), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message': 'Block added successfully to the peer nodes'}
            return jsonify(response), 201
        else:
            response = { 'message': 'Block failed to be added to the peer nodes'}
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
      response = {'message': 'Blockchain seems to differ from the local blockchain'}
      blockchain.resolve_conflicts = True
      return jsonify(response), 200
    else:
      response = {'message': 'Blockchain seems to be shorter'}
      return jsonify(response), 409

@app.route('/transaction', methods=['POST'])
def add_transaction():
    values = request.get_json()
    required_fields = ['recipient', 'amount']
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
    blockchain = Blockchain(public_key, port)
    receiver = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(public_key, receiver, amount)
    if blockchain.add_transaction(receiver, public_key, signature, amount=amount):
        response = {
            'funds': blockchain.get_balance(),
            'message': 'Transaction successfull',
            'transaction': {
                'sender': public_key,
                'recipient': receiver,
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
        block_dict = ConverterToDict.block_to_dict(block)
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
    chain_dict = ConverterToDict.chain_to_dict(chain_snapshot)
    return jsonify(chain_dict), 200


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data attached'
        }
        return jsonify(response), 400
    if not 'node' in values:
        response = {
            'message': 'No data attached'
        }
        return jsonify(response), 400
    node = values['node']
    blockchain.add_peer_node(node)
    response = {
        'message': 'Peer node added successfully',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201


@app.route('/node/<node_url>', methods=['DELETE'])
def delete_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': 'No node URL passed'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node removed successfully',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


@app.route('/nodes', methods=['GET'])
def get_nodes():
    response = {
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port)
