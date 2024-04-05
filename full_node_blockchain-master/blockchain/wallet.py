import rsa
import binascii

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


class Address:
    def __init__(self, addr):
        if isinstance(addr, rsa.PublicKey):
            self.addr = addr
        else:
            if isinstance(addr,str):
                addr = addr.encode()
            # thats not clean bu i didnt find simple crypto library for 512 sha key
            # to get address/public_key short. 
            self.addr = rsa.PublicKey.load_pkcs1(b'-----BEGIN RSA PUBLIC KEY-----\n%b\n-----END RSA PUBLIC KEY-----\n' % addr)

    def __str__(self):
        return b''.join(self.addr.save_pkcs1().split(b'\n')[1:-2]).decode()

    @property
    def key(self):
        return self.addr

class Wallet:
    '''For real case wallet use ECDSA cryptography'''

    __slots__ = '_pub', '_priv'
    
    def __init__(self, pub=None, priv=None):
        if pub:
            self._pub = Address(pub)
            self._priv = rsa.PrivateKey.load_pkcs1(priv)

    @classmethod
    def create(cls):
        inst = cls(b'',b'')
        _pub, _priv = rsa.newkeys(512)
        inst._pub = Address(_pub)
        inst._priv = _priv
        return inst

    @classmethod
    def verify(cls, data, signature, address):
        signature = binascii.unhexlify(signature.encode())
        if not isinstance(address, Address):
            address = Address(address)
        try:
            return rsa.verify(data, signature, address.key) == 'SHA-256'
        except:
            return False 
    
    @property
    def address(self):
        return str(self._pub)

    @property
    def priv(self):
        return self._priv.save_pkcs1()

    def sign(self, hash):
        return binascii.hexlify(rsa.sign(hash, self._priv, 'SHA-256')).decode()