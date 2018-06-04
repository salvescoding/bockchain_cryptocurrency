blockchain = []


def last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_value(transaction, last_transaction=[0]):
    if last_transaction == None:
        last_transaction = [0]
    blockchain.append([last_transaction, transaction])


def get_transaction_value():
    return float(input('Please enter the ammount you would like to transfer: '))


def get_user_choice():
    return input('Your choice  ')


def print_blockchain_elements():
    for block in blockchain:
        print("Block number")
        print(block)


def verify_chain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid


while True:
    print('Pease Choose:')
    print('1 - Add a new transaction')
    print('2 - Print your blockchain')
    print('3 - Manipulate the chain')
    print('4 - Quit')
    choice = get_user_choice()
    if choice == '1':
        add_value(get_transaction_value(), last_blockchain_value())
    elif choice == '2':
        print_blockchain_elements()
    elif choice == '3':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif choice == '4':
        break
    else:
        print('Invalid option, please choose a number from the list')
    if not verify_chain():
        print("Invalid Blockchain")
        break

print("Done")
