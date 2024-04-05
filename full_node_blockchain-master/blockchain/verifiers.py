import rsa
import binascii

from .wallet import Address

"""
This module provides classes for verifying transactions and blocks within a blockchain system. It ensures
the integrity and validity of transactions and blocks before they are added to the blockchain.

Classes:
    TxVerifier:
        Verifies the validity of transactions by checking digital signatures, ensuring inputs refer to unspent
        transaction outputs (UTXOs), and validating the input amounts against output amounts.

    BlockVerifier:
        Verifies the validity of blocks by checking the block's hash against the target difficulty, verifying
        all transactions within the block, and ensuring the block reward is correctly calculated.

Exceptions:
    BlockOutOfChain:
        Raised when an attempt is made to add a block that does not properly link to the existing blockchain.

    BlockVerificationFailed:
        Raised when a block fails to meet the blockchain's difficulty requirements or contains invalid transactions.

Usage:
    The `TxVerifier` and `BlockVerifier` classes are utilized within the blockchain's addition process to
    ensure that only valid transactions and blocks are appended to the blockchain. They are crucial for
    maintaining the blockchain's integrity and security.

Example:
    db = DB() # Assume DB is an initialized database instance for blockchain state
    tx_verifier = TxVerifier(db)
    try:
        fee = tx_verifier.verify(transaction.inputs, transaction.outputs)
    except Exception as e:
        # Handle invalid transaction

    block_verifier = BlockVerifier(db)
    try:
        block_verifier.verify(previous_block, new_block)
    except BlockOutOfChain as e:
        # Handle block out of chain error
    except BlockVerificationFailed as e:
        # Handle block verification failure

Note:
    Verification processes involve cryptographic operations such as digital signature verification. It requires
    access to the blockchain's current state through the `db` instance to check UTXOs and other transaction
    and block attributes.
"""


class TxVerifier:
    def __init__(self, db):
        self.db = db

    def verify(self, inputs, outputs):
        total_amount_in = 0
        total_amount_out = 0
        for i,inp in enumerate(inputs):
            if inp.prev_tx_hash == 'COINBASE' and i == 0:
                total_amount_in = int(self.db.config['mining_reward'])
                continue
 
            try:
                out = self.db.transaction_by_hash[inp.prev_tx_hash]['outputs'][inp.output_index]
            except KeyError:
                raise Exception('Transaction output not found.')

            total_amount_in += int(out['amount'])

            if (inp.prev_tx_hash,out['hash']) not in self.db.unspent_txs_by_user_hash.get(out['address'], set()):
                raise Exception('Output of transaction already spent.')

            hash_string = '{}{}{}{}'.format(
                inp.prev_tx_hash, inp.output_index, inp.address, inp.index
            )
            try:
                rsa.verify(hash_string.encode(), binascii.unhexlify(inp.signature.encode()), Address(out['address']).key) == 'SHA-256'
            except:
                raise Exception('Signature verification failed: %s' % inp.as_dict)

        for out in outputs:
            total_amount_out += int(out.amount)

        if total_amount_in < total_amount_out:
            raise Exception('Insuficient funds.')

        return total_amount_in - total_amount_out

class BlockOutOfChain(Exception):
    pass

class BlockVerificationFailed(Exception):
    pass

class BlockVerifier:
    def __init__(self, db):
        self.db = db
        self.tv = TxVerifier(db)

    def verify(self, head, block):
        total_block_reward = int(self.db.config['mining_reward'])

        # verifying block hash
        if int(block.hash(), 16) > (2 ** (256-self.db.config['difficulty'])):
            raise BlockVerificationFailed('Block hash bigger then target difficulty')     

        # verifying transactions in a block
        for tx in block.txs[1:]:
            fee = self.tv.verify(tx.inputs, tx.outputs)
            total_block_reward += fee
        
        total_reward_out = 0
        for out in block.txs[0].outputs:
            total_reward_out += out.amount

        # verifying block reward
        if total_block_reward != total_reward_out:
            raise BlockVerificationFailed('Wrong reward sum')
        
        # verifying some other things
        if head:
            if head.index >= block.index:
                raise BlockOutOfChain('Block index number wrong')
            if head.hash() != block.prev_hash:
                raise BlockOutOfChain('New block not pointed to the head')
            if head.timestamp > block.timestamp:
                raise BlockOutOfChain('Block from the past')

        return True
