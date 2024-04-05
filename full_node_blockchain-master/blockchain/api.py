from .blocks import Tx, Block

"""
The API class serves as a high-level interface to the blockchain functionality. It allows interaction with the 
blockchain through a series of methods that handle user balances, transactions, blocks, and the mining process.

Methods:
    __init__(self, blockchain):
        Initializes the API with a reference to an instance of a blockchain.

    get_user_balance(self, address):
        Calculates and returns the total balance of a given address by summing up the value of unspent transaction outputs.

    get_user_unspent_txs(self, address):
        Retrieves a list of unspent transactions for a given address, including details such as transaction hash, 
        output index, output hash, and the amount.

    get_chain(self, from_block: int, limit: int = 20):
        Returns a portion of the blockchain starting from a specified block index, limited to a certain number of blocks. 
        It also includes blocks from any potential forks (splitbrain situations).

    add_block(self, block):
        Adds a new block to the blockchain. If the block is valid and accepted, it triggers any necessary rollover logic.

    mine_block(self, check_stop=None):
        Initiates the block mining process. An optional callback can be provided to stop mining as needed.

    add_tx(self, tx):
        Adds a new transaction to the blockchain's pool of unconfirmed transactions.

    get_head(self):
        Retrieves and returns the latest block in the blockchain as a dictionary.

Usage:
    This class is intended to be used within a FastAPI application to provide HTTP endpoints that interact with the 
    blockchain. It abstracts and encapsulates blockchain operations without altering the core blockchain code.

Note:
    The methods of the API class depend on the internal structure and methods of the blockchain and transaction 
    classes (`Block` and `Tx`). If these components are modified, corresponding changes in the API class may be required.
"""


class API:

    """
        Some wrapper around blockchain to add some logic without changing
        main blockchain code
    """

    def __init__(self, blockcain):
        self.bc = blockcain

    def get_user_balance(self, address):
        total = 0
        for v in self.bc.db.unspent_outputs_amount[str(address)].values():
            total += v
        return total

    def get_user_unspent_txs(self, address):
        res = []
        for tx_hash,out_hash in self.bc.db.unspent_txs_by_user_hash[str(address)]:
            amount = self.bc.db.unspent_outputs_amount[str(address)][out_hash]
            for index,out in enumerate(self.bc.db.transaction_by_hash[tx_hash]['outputs']):
                if out['hash'] == out_hash:
                    res.append({
                        "tx": tx_hash,
                        "output_index": index,
                        "out_hash": out_hash,
                        "amount": amount
                    })
        return res

    def get_chain(self, from_block:int, limit:int=20):
        res = [b.as_dict for b in self.bc.chain[from_block:from_block+limit]]
        # adding blocks from splitbrain
        if len(res) < limit:
            res += self.bc.fork_blocks.values()
        return res

    def add_block(self, block):
        block = Block.from_dict(block)
        res = self.bc.add_block(block)
        if res:
            self.bc.rollover_block(block)
        return res

    def mine_block(self, check_stop=None):
        self.bc.force_block(check_stop)

    def add_tx(self, tx):
        return self.bc.add_tx(Tx.from_dict(tx))

    def get_head(self):
        if not self.bc.head:
            return {}
        return self.bc.head.as_dict
            