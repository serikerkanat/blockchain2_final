import hashlib
import json
from time import time
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class CharityBlockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            timestamp=time(),
            data={'message': 'Genesis Block'},
            previous_hash='0'
        )
        self.chain.append(genesis_block)

    def add_transaction(self, donor: str, amount: float, recipient: str, purpose: str):
        transaction = {
            'donor': donor,
            'amount': amount,
            'recipient': recipient,
            'purpose': purpose,
            'timestamp': time()
        }
        
        last_block = self.chain[-1]
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time(),
            data=transaction,
            previous_hash=last_block.hash
        )
        
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def get_transaction_history(self, donor: str = None, recipient: str = None) -> List[Dict]:
        history = []
        for block in self.chain[1:]:  # Skip genesis block
            if donor and block.data['donor'] != donor:
                continue
            if recipient and block.data['recipient'] != recipient:
                continue
            history.append(block.data)
        return history
