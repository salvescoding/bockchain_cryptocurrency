blockchain = []


def last_blockchain_value():
    return blockchain[-1]


def add_value(transaction, last_transaction=[0]):
    blockchain.append([last_transaction, transaction])


def get_transaction_value():
    return float(input('Please enter the ammount you would like to transfer: '))


def get_user_choice():
    input('Your choice  ')


add_value(get_transaction_value())


while True:
    print('Pease Choose:')
    print('1 - Add a new transaction')
    print('2 - Print your blockchain')
    choice = get_user_choice()
    if choice == '1':
        add_value(get_transaction_value(),
                  last_blockchain_value())
    else:
        for block in blockchain:
            print("Block number")
            print(block)


print("Done")
