from blockchain import (Block, Blockchain)

def print_help():
    print("The currently support actions are as follows: ")
    print("`help` - Lists this menu")
    print("`verify` - Verifies that the blockchain is in a valid state")
    print("`mine` - Mine a new block and insert it into the blockchain")
    print("`print` - Prints the current blockchain")
    print("`exit` - Exits this input loop")
    print("`quit` - Same thing as exit")

def main():
    print("Creating the blockchain...")
    data = input("Creating the genesis block. What would you like it's data to be?: ")
    genesis_block = Block("0", data)
    chain = Blockchain(genesis_block)

    print("Genesis block hash: ", genesis_block.hash)
    action = input("What would you like to do? To get a list of options, type 'help': ").lower()
    while(action != "quit" and action != "exit"):
        if action == "help":
            print_help()

        elif action == "verify":
            if chain.check_integrity():
                print("The current blockchain is valid.")
            else:
                print("The current blockchain is not in a valid state.")

        elif action == "mine":
            chain.mine_block()

        elif action == "print":
            chain.print_chain()
        else:
            print("Hmmmm, not sure what you meant. Type `help` to get a list of comamands.")

        action = input("What would you like to do? ")
    

if __name__ == "__main__":
    main()