import pickle
from collections import defaultdict

"""
A simple database emulation class for storing blockchain data. It manages configurations, transactions, 
and unspent transaction outputs (UTXOs) using in-memory structures. Additionally, it provides mechanisms 
for persisting and restoring the database state.

Attributes:
    config (dict): Configuration settings for the blockchain, including the number of transactions per block,
                   mining rewards, and difficulty level.
    block_index (int): The current block index in the blockchain.
    transaction_by_hash (dict): A mapping from transaction hashes to transaction data.
    unspent_txs_by_user_hash (defaultdict(set)): A mapping from user addresses to sets of unspent transaction hashes.
    unspent_outputs_amount (defaultdict(dict)): A mapping from user addresses to dictionaries mapping output hashes to amounts, 
                                                representing unspent outputs available for spending.

Methods:
    backup(self):
        Serializes and saves the current state of the database to a file named after the current block index. 
        Uses Python's `pickle` module for serialization.

    restore(block_index: int) -> 'DB':
        A class method that deserializes and restores the database state from a file corresponding to the specified block index. 
        Returns an instance of `DB` with the restored state.

Usage:
    This class is intended to be used within a blockchain system to store and manage the state of the blockchain, including 
    transactions and UTXOs. It provides simple methods for persisting the blockchain state across sessions, aiding in 
    development and testing scenarios.

Example:
    # Creating a new database instance and configuring blockchain parameters
    db = DB()

    # Backup the current state after adding transactions and blocks
    db.backup()

    # Restore the database state to a specific block index
    restored_db = DB.restore(block_index=10)

Note:
    The `backup` and `restore` methods rely on the file system for data persistence, and use Python's `pickle` module, 
    which is not secure against erroneous or maliciously constructed data. Never unpickle data from an untrusted or 
    unauthenticated source.
"""


class DB:
    """
    Class that just emulates some sort of DB used to save all data
    """
    def __init__(self):
        self.config = {
            'txs_per_block': 4,
            'mining_reward': 25,
            'difficulty': 22,
        }

        self.block_index = 0
        self.transaction_by_hash = {}
        self.unspent_txs_by_user_hash = defaultdict(set)
        self.unspent_outputs_amount = defaultdict(dict)

    '''
        Just simple routine to save/restore db data for block number
    '''
    def backup(self):
        with open('block_%s' % self.block_index,'wb') as fp:
            pickle.dump(self.__dict__, fp)

    @classmethod
    def restore(cls, block_index):
        with open('block_%s' % block_index, 'rb') as fp:
            data = pickle.load(fp)

        inst = cls()
        inst.__dict__ = data
        return inst