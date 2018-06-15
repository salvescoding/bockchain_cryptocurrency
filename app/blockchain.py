import functools
import hashlib as hl
from collections import OrderedDict

from hash_util import hash_block, hash_string_256

MINING_REWARD = 10
genesis_block = {
    'prv_block_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Sergio'
participants = {'Sergio'}



def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    transaction_sender = [[tx['amount'] for tx in block['transactions']
                           if tx['sender'] == participant] for block in blockchain]
    open_transactions_sender = [tx['amount']
                                for tx in open_transactions if tx['sender'] == participant]
    transaction_sender.append(open_transactions_sender)
    print(transaction_sender)
    amount_sent = functools.reduce(
        lambda memo, el: memo + sum(el) if len(el) > 0 else memo + 0,                             transaction_sender, 0)
    transaction_recipient = [[tx['amount'] for tx in block['transactions']
                              if tx['receiver'] == participant] for block in blockchain]
    amount_received = functools.reduce(
        lambda memo, el: memo + sum(el) if len(el) > 0 else memo + 0,
        transaction_recipient, 0)

    return amount_received - amount_sent


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(receiver, sender=owner, amount=1):
    # transaction = {
    #     'sender': sender,
    #     'receiver': receiver,
    #     'amount': amount
    # }
    transaction = OrderedDict(
        [('sender', sender), ('receiver', receiver), ('amount', amount)])
    print(transaction)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(receiver)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # mine_reward = {
    #     'sender': 'MINING',
    #     'receiver': owner,
    #     'amount': MINING_REWARD
    # }
    mine_reward = OrderedDict(
        [('sender', 'MINING'), ('receiver', owner), ('amount', MINING_REWARD)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(mine_reward)
    block = {'prv_block_hash': hashed_block,
             'index': len(blockchain),
             'transactions': copied_transactions,
             'proof': proof
             }
    blockchain.append(block)
    return True


def get_transaction_value():
    receiver = input('Please enter the receiver: ')
    amount = float(
        input('Please enter the ammount you would like to transfer: '))
    return (receiver, amount)


def get_user_choice():
    return input('Your choice  ')


def print_blockchain_elements():
    for block in blockchain:
        print("Block number")
        print(block)
    else:
        print('-' * 30)


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['prv_block_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['prv_block_hash'], block['proof']):
            print('Proof of work is invalid')
            return False
    return True


def verify_all_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    print('Pease Choose:')
    print('1 - Add a new transaction')
    print('2 - Mine the block')
    print('3 - Print your blockchain')
    print('4 - Manipulate the chain')
    print('5 - Print the participants')
    print('6 - Check transactions are valid')
    print('7 - Quit')
    choice = get_user_choice()
    if choice == '1':
        transaction_data = get_transaction_value()
        receiver, amount = transaction_data
        if add_transaction(receiver, amount=amount):
            print('Transaction completed!')
        else:
            print('Transaction Failed!')
        print(open_transactions)
    elif choice == '2':
        if mine_block():
            open_transactions = []
    elif choice == '3':
        print_blockchain_elements()
    elif choice == '4':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'prv_block_hash': '',
                'index': 0,
                'transactions': {'sender': 'Marise', 'receiver': 'Sergio', 'amount': 100.0}
            }
    elif choice == '5':
        print(participants)
    elif choice == '6':
        if verify_all_transactions():
            print('All transactions are valid')
        else:
            print("You have invalid transactions")
    elif choice == '7':
        waiting_for_input = False
    else:
        print('Invalid option, please choose a number from the list')
    if not verify_chain():
        print_blockchain_elements()
        print("Invalid Blockchain")
        break
    print("{} balance is: {:6.2f} coins".format(owner, get_balance(owner)))
else:
    print('Thank you for using our service')
