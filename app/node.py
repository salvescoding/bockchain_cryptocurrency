class Node:


    def __init__(self):
        self.blockchain = []

    def get_transaction_value(self):
        receiver = input('Please enter the receiver: ')
        amount = float(
            input('Please enter the ammount you would like to transfer: '))
        return (receiver, amount)

    def get_user_choice(self):
        return input('Your choice  ')

    def print_blockchain_elements(self):
        for block in self.blockchain:
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
            print('5 - Quit')
            choice = self.get_user_choice()
            if choice == '1':
                transaction_data = self.get_transaction_value()
                receiver, amount = transaction_data
                if add_transaction(receiver, amount=amount):
                    print('Transaction completed!')
                else:
                    print('Transaction Failed!')
                print(open_transactions)
            elif choice == '2':
                if mine_block():
                    open_transactions = []
                    save_data()
            elif choice == '3':
                self.print_blockchain_elements()
            elif choice == '4':
                verify = Verification()
                if verify.verify_all_transactions(open_transactions, get_balance):
                    print('All transactions are valid')
                else:
                    print("You have invalid transactions")
            elif choice == '5':
                waiting_for_input = False
            else:
                print('Invalid option, please choose a number from the list')
            verify = Verification()
            if not verify.verify_chain(self.blockchain):
                self.print_blockchain_elements()
                print("Invalid Blockchain")
                break
            print("{} balance is: {:6.2f} coins".format(
                owner, get_balance(owner)))
        else:
            print('Thank you for using our service')
