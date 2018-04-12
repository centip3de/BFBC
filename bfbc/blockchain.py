import string
import random
from datetime import datetime
from hashlib import sha256

class Block:
    def __init__(self, previous_hash, data):
        self.previous_hash = str(previous_hash).encode("utf-8")
        self.data = str(data).encode("utf-8")
        self.timestamp = str(datetime.now()).encode("utf-8")
        self.hash = self.calculate_hash()
        self.next_block = None

    def calculate_hash(self):
        m = sha256()
        m.update(self.previous_hash + self.timestamp + self.data)
        return str(m.hexdigest())

    def set_next_block(self, block):
        self.next_block = block

class Blockchain:
    def __init__(self, genesis_block):
        self.genesis_block = genesis_block
        self.head = genesis_block
        self.proof_of_work_difficulty = 4

    def add_block_from_data(self, data):
        new_block = Block(self.head.hash, data)
        self.head.next_block = new_block
        self.head = new_block

    def add_block(self, block):
        self.head.next_block = block
        self.head = block

    def print_chain(self):
        current_block = self.genesis_block
        while(current_block is not None):
            print("{")
            print("\tPrevious block hash:", current_block.previous_hash)
            print("\tBlock hash:", current_block.hash)
            print("\tBlock data:", current_block.data)
            print("\tBlock timestamp:", current_block.timestamp)
            print("},")
            current_block = current_block.next_block

    def check_integrity(self):
        previous_block = None
        current_block = self.genesis_block
        while(current_block.next_block is not None):
            if current_block.hash != current_block.calculate_hash():
                print("Improper hash")
                return False

            if current_block.hash[0:self.proof_of_work_difficulty] != "0"*self.proof_of_work_difficulty:
                print("Unmined block")
                return False
            
            if previous_block:
                if previous_block.hash != current_block.previous_hash.decode("utf-8"):
                    print("Improper hash")
                    return False

            previous_block = current_block
            current_block = current_block.next_block

        print("Valid blockchain")
        return True

    def mine_block(self):
        data = input("What data would you like to store on this block? ")
        new_block = Block(self.head.hash, data)
        target = "0"*self.proof_of_work_difficulty
        while(new_block.hash[0:self.proof_of_work_difficulty] != target):
            new_block = Block(self.head.hash, data)

        print("New block mined!")
        print("New block has hash:", new_block.hash)
        self.add_block(new_block)

        answer = input("Would you like to mine another block? [Y/N]: ")
        if answer.lower() == "y":
            self.mine_block()
