class ConverterToDict():

    @staticmethod
    def chain_to_dict(chain):
        chain_dict = [block.__dict__.copy() for block in chain]
        for block_dict in chain_dict:
            block_dict['transactions'] = [tx.__dict__ for tx in block_dict['transactions']]
        return chain_dict

    @staticmethod
    def block_to_dict(block):
        block_dict = block.__dict__.copy()
        block_dict['transactions'] = [
            tx.__dict__ for tx in block_dict['transactions']]
        return block_dict

    @staticmethod
    def transactions_to_dict(transactions):
        dict_transactions = [tx.__dict__ for tx in transactions]
        return dict_transactions
