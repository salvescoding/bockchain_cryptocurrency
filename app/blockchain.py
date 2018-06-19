import functools
import hashlib as hl
import json
import pickle

from hash_util import hash_block, hash_string_256
from block import Block
from transaction import Transaction
from verification import Verification


MINING_REWARD = 10


class Blockchain:

    def __init__(self, hosting_node):
        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['open_transactions']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['receiver'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['receiver'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.open_transactions = updated_transactions
        except (IOError, IndexError):
            print('Handled exception')
        finally:
            print('Cleanup')

    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                # Save data as JSON format
                savable_blockchain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                    tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.chain]]
                f.write(json.dumps(savable_blockchain))
                f.write('\n')
                savable_open_transactions = [
                    tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(savable_open_transactions))
                # Save data as binary
                # save_data = {
                #   'chain': blockchain,
                #   'open_transactions': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        verify = Verification()
        while not verify.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        participant = self.hosting_node
        transaction_sender = [[tx.amount for tx in block.transactions
                               if tx.sender == participant] for block in self.chain]
        open_transactions_sender = [tx.amount
                                    for tx in self.open_transactions if tx.sender == participant]
        transaction_sender.append(open_transactions_sender)
        print(transaction_sender)
        amount_sent = functools.reduce(
            lambda memo, el: memo + sum(el) if len(el) > 0 else memo + 0,                             transaction_sender, 0)
        transaction_recipient = [[tx.amount for tx in block.transactions
                                  if tx.receiver == participant] for block in self.chain]
        amount_received = functools.reduce(
            lambda memo, el: memo + sum(el) if len(el) > 0 else memo + 0,
            transaction_recipient, 0)

        return amount_received - amount_sent

    def last_blockchain_value(self):
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, receiver, sender, amount=1):
        # transaction = {
        #     'sender': sender,
        #     'receiver': receiver,
        #     'amount': amount
        # }
        transaction = Transaction(sender, receiver, amount)
        print(transaction)
        verify = Verification()
        if verify.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # mine_reward = {
        #     'sender': 'MINING',
        #     'receiver': owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.chain), hashed_block,
                      copied_transactions, proof)
        self.chain.append(block)
        self.open_transactions = []
        self.save_data()
        return True
