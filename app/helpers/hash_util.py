import hashlib as hl
import json

def hash_string_256(string):
    return hl.sha256(string).hexdigest()

def hash_block(block):
    hashed_block = block.__dict__.copy()
    hashed_block['transactions'] = [
        tx.to_ordered_dict() for tx in hashed_block['transactions']]
    return hash_string_256(json.dumps(hashed_block, sort_keys=True).encode())
