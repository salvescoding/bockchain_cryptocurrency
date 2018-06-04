blockchain = []
open_transactions = []
owner = 'Sergio'


def last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(sender, receiver, amount=1):
    transaction = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount
    }
    open_transactions.append(transaction)


def mine_block():
    pass


def get_transaction_value():
    receiver = input('Please enter the receiver: ')
    amount = float(input('Please enter the ammount you would like to transfer: '))
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
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            print(blockchain[block_index][0])
            print(blockchain[block_index - 1])
            is_valid = True
        else:
            is_valid = False
    return is_valid


waiting_for_input = True

while waiting_for_input:
    print('Pease Choose:')
    print('1 - Add a new transaction')
    print('2 - Print your blockchain')
    print('3 - Manipulate the chain')
    print('4 - Quit')
    choice = get_user_choice()
    if choice == '1':
        transaction_data = get_transaction_value()
        add_transaction(transaction_data, last_blockchain_value())
    elif choice == '2':
        print_blockchain_elements()
    elif choice == '3':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif choice == '4':
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
