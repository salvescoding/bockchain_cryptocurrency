from block import Block
from transaction import Transaction

class ConverterToObj():

  @staticmethod
  def chain_to_obj(blockchain):
      """
      Receives a blockchain of dictionaries and converts the blocks
      into block objects and the transactions into Transactions objects
      Returns an updated blockchain of objects
      """
      updated_blockchain = []
      for block in blockchain:
          converted_tx = [Transaction(
              tx['sender'], tx['receiver'], tx['signature'], tx['amount']) for tx in block['transactions']]
          updated_block = Block(
              block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
          updated_blockchain.append(updated_block)
      return updated_blockchain

  @staticmethod
  def transaction_dict_to_obj(transactions):
      """
      Converts a set of transactions dictionaries to Transaction object
      Arguments:
      - An Array of transactions
      """
      updated_transactions = []
      for tx in transactions:
          updated_transaction = Transaction(
              tx['sender'], tx['receiver'], tx['signature'], tx['amount'])
          updated_transactions.append(updated_transaction)
      return updated_transactions

