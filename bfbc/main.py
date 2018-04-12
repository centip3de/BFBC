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

    def add_block(self, data):
        new_block = Block(self.head.hash, data)
        self.head.next_block = new_block
        self.head = new_block

    def check_integrity(self):
        previous_block = None
        current_block = self.genesis_block
        while(current_block.next_block is not None):
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if previous_block:
                if previous_block.hash != current_block.previous_hash.decode("utf-8"):
                    return False

            previous_block = current_block
            current_block = current_block.next_block

        return True

def main():
    genesis_block = Block("0", "I'm the first block")
    chain = Blockchain(genesis_block)
    chain.add_block("I'm the second block!")
    chain.add_block("I'm the third block!")
    chain.add_block("I'm the fourth block!")

    print("Genesis block hash: ", genesis_block.hash)
    print("Integrity:", chain.check_integrity())
    

if __name__ == "__main__":
    main()