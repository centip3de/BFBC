import string
import random
from datetime import datetime
from hashlib import sha256

class Block:
    def __init__(self, previous_hash, data):
        # Get the required pieces to calculate the hash.
        # NOTE: We're encoding them here solely because that's what the SHA256 function requires
        self.previous_hash = str(previous_hash).encode("utf-8")
        self.data = str(data).encode("utf-8")
        self.timestamp = str(datetime.now()).encode("utf-8")

        # After we've added the required peices, we can now calculate the hash
        self.hash = self.calculate_hash()
        self.next_block = None

    def calculate_hash(self):
        # Calculate the hash and return it in a somewhat human-readable form
        m = sha256()
        m.update(self.previous_hash + self.timestamp + self.data)
        return str(m.hexdigest())

class Blockchain:
    def __init__(self, genesis_block):
        self.genesis_block = genesis_block
        self.head = genesis_block
        self.proof_of_work_difficulty = 4

    def add_block_from_data(self, data):
        # Create a new block object and add it
        new_block = Block(self.head.hash, data)
        self.head.next_block = new_block
        self.head = new_block

    def add_block(self, block):
        # Add a proper block
        self.head.next_block = block
        self.head = block

    def print_chain(self):
        # Print out the chain in a JSON-esque format
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

            # Make sure that the hashes are calculated as we expect
            if current_block.hash != current_block.calculate_hash():
                print("Improper hash")
                return False

            # Make sure that all the hashes have done the work required
            if current_block.hash[0:self.proof_of_work_difficulty] != "0"*self.proof_of_work_difficulty:

                # The genesis block doesn't obey by they same rules, so just ignore it for this check
                if current_block.previous_hash != b"0":
                    print("Unmined block")
                    return False
            
            # Make sure our "previous_hash" field is pointing to the correct block
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

        # Here we implement mining a new block. The mining scheme we're using is Proof of Work.
        # The implementation here is a simple version of hashcat, which is used by Bitcoin and Ethereum:
        # we calculate random hashes until one of them has the correct amount of leading 0's.
        # The correct amount is dictated by the proof_of_work_difficulty variable. If you want to increase/decrease
        # mining times, change that variable
        target = "0"*self.proof_of_work_difficulty
        while(new_block.hash[0:self.proof_of_work_difficulty] != target):
            new_block = Block(self.head.hash, data)

        print("New block mined!")
        print("New block has hash:", new_block.hash)
        self.add_block(new_block)

        answer = input("Would you like to mine another block? [Y/N]: ")
        if answer.lower() == "y":
            self.mine_block()
