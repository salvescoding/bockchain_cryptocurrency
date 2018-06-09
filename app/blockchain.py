genesis_block = {
    'prv_block_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Sergio'
participants = {'Sergio'}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(receiver, sender=owner, amount=1):
    transaction = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount
    }
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(receiver)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    print(hashed_block)
    block = {'prv_block_hash': hashed_block,
             'index': len(blockchain),
             'transactions': open_transactions
             }
    blockchain.append(block)


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
    return True


waiting_for_input = True

while waiting_for_input:
    print('Pease Choose:')
    print('1 - Add a new transaction')
    print('2 - Mine the block')
    print('3 - Print your blockchain')
    print('4 - Manipulate the chain')
    print('5 - Print the participants')
    print('6 - Quit')
    choice = get_user_choice()
    if choice == '1':
        transaction_data = get_transaction_value()
        receiver, amount = transaction_data
        add_transaction(receiver, amount=amount)
        print(open_transactions)
    elif choice == '2':
        mine_block()
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
        waiting_for_input = False
    else:
        print('Invalid option, please choose a number from the list')
    if not verify_chain():
        print_blockchain_elements()
        print("Invalid Blockchain")
        break
else:
    print('Thank you for using our service')

print("Done")
