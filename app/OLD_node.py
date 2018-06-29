from uuid import uuid4

from blockchain import Blockchain
from helpers.verification import Verification
from wallet import Wallet


class Node:

    def __init__(self):
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_value(self):
        receiver = input('Please enter the receiver: ')
        amount = float(
            input('Please enter the ammount you would like to transfer: '))
        return (receiver, amount)

    def get_user_choice(self):
        return input('Your choice  ')

    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print("Block number")
            print(block)
        else:
            print('-' * 30)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('Pease Choose:')
            print('1 - Add a new transaction')
            print('2 - Mine the block')
            print('3 - Print your blockchain')
            print('4 - Check transactions are valid')
            print('5 - Create Wallet')
            print('6 - Load Wallet')
            print('7 - Save keys')
            print('q - Quit')
            choice = self.get_user_choice()
            if choice == '1':
                transaction_data = self.get_transaction_value()
                receiver, amount = transaction_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, receiver, amount)
                if self.blockchain.add_transaction(receiver, self.wallet.public_key, signature, amount=amount):
                    print('Transaction completed!')
                else:
                    print('Transaction Failed!')
                print(self.blockchain.get_open_transactions())
            elif choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining a new block failed! Got not wallet?')
            elif choice == '3':
                self.print_blockchain_elements()
            elif choice == '4':
                if Verification.verify_all_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print("You have invalid transactions")
            elif choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif choice == '7':
                self.wallet.save_keys()
            elif choice == 'q':
                waiting_for_input = False
            else:
                print('Invalid option, please choose a number from the list')
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("Invalid Blockchain")
                break
            print("{} balance is: {:6.2f} coins".format(
                self.wallet.public_key, self.blockchain.get_balance()))
        else:
            print('Thank you for using our service')


node = Node()
node.listen_for_input()
