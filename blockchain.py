blockchain = []


def last_blockchain_value():
    return blockchain[-1]


def add_value(transaction, last_transaction=[0]):
    blockchain.append([last_transaction, transaction])


def user_input():
    return float(input('Please enter the ammount you would like to transfer: '))


add_value(user_input())

add_value(last_transaction=last_blockchain_value(),
          transaction=user_input())

add_value(user_input(),
          last_blockchain_value())

print(blockchain)
