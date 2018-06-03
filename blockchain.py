blockchain = []


def last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_value(transaction, last_transaction=[0]):
    blockchain.append([last_transaction, transaction])


def get_transaction_value():
    return float(input('Please enter the ammount you would like to transfer: '))


def get_user_choice():
    return input('Your choice  ')


def print_blockchain_elements():
    for block in blockchain:
        print("Block number")
        print(block)


add_value(get_transaction_value())


while True:
    print('Pease Choose:')
    print('1 - Add a new transaction')
    print('2 - Print your blockchain')
    print('3 - Quit')
    choice = get_user_choice()
    if choice == '1':
        add_value(get_transaction_value(), last_blockchain_value())
    elif choice == '2':
        print_blockchain_elements()
    elif choice == '3':
        break
    else:
        print('Invalid option, please choose a number from the list')
    print('Choice Registered')


print("Done")
