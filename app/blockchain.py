import functools
import hashlib as hl
import json
import pickle
import requests

from helpers.hash_util import hash_block
from helpers.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet


MINING_REWARD = 10


class Blockchain:

    def __init__(self, public_key, node_id):
        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.public_key = public_key
        self.node_id = node_id
        self.__peer_nodes = set()
        self.resolve_conflicts = False
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain-{0}.txt'.format(self.node_id), mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['open_transactions']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['receiver'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['receiver'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            print('Handled exception')
        finally:
            print('Cleanup')

    def save_data(self):
        try:
            with open('blockchain-{0}.txt'.format(self.node_id), mode='w') as f:
                # Save data as JSON format
                savable_blockchain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                    tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(savable_blockchain))
                f.write('\n')
                savable_open_transactions = [
                    tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(savable_open_transactions))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
                # Save data as binary
                # save_data = {
                #   'chain': blockchain,
                #   'open_transactions': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self, sender=None):
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
        transaction_sender = [[tx.amount for tx in block.transactions
                               if tx.sender == participant] for block in self.__chain]
        open_transactions_sender = [tx.amount
                                    for tx in self.__open_transactions if tx.sender == participant]
        transaction_sender.append(open_transactions_sender)
        print(transaction_sender)
        amount_sent = functools.reduce(
            lambda memo, el: memo + sum(el) if len(el) > 0 else memo + 0,                             transaction_sender, 0)
        transaction_recipient = [[tx.amount for tx in block.transactions
                                  if tx.receiver == participant] for block in self.__chain]
        amount_received = functools.reduce(
            lambda memo, el: memo + sum(el) if len(el) > 0 else memo + 0,
            transaction_recipient, 0)

        return amount_received - amount_sent

    def last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, receiver, sender, signature, amount=1, is_receiving=False):
        # if self.public_key == None:
        #     return False
        transaction = Transaction(sender, receiver, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{0}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={
                                                 'sender': sender, 'receiver': receiver, 'amount': amount, 'signature': signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print("Transaction declined, needs resolving")
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def add_block(self, block):
        transactions = [Transaction(
            tx['sender'], tx['receiver'], tx['signature'], tx['amount']) for tx in block['transactions']]
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        convert_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
        self.__chain.append(convert_block)
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if itx['sender'] == opentx.sender and itx['receiver'] == opentx.receiver and itx['amount'] == opentx.amount and itx['signature'] == opentx.signature:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Transaction has already been removed')
        self.save_data()
        return True

    def mine_block(self):
        if self.public_key == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            'MINING', self.public_key, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = "http://{0}/broadcast-block".format(node)
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [
                tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print("Block declined")
                if response.status_code == 409:
                    self.resolve_conflicts = True

            except requests.exceptions.ConnectionError:
                continue

        return block

    def add_peer_node(self, node):
        """Adds a new peer node to the node set

            Arguments:
                :node: The node URL should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """ Removes the node passed in the arguments """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """ Returns a list of all peer nodes"""
        return list(self.__peer_nodes)
