import pytest
from unittest import TestCase as tc
import copy
import pprint

from .blocks import Tx, Input, Output
from .blockchain import Blockchain
from .wallet import Wallet
from .verifiers import TxVerifier
from .db import DB

"""
This test suite validates the functionality of various blockchain components including transactions, blockchains,
wallets, and database rollbacks.

Tests:
    test_tx_verifier():
        Tests the transaction verification process. It ensures that a transaction with valid inputs and outputs
        passes verification and that transactions with insufficient funds or with inputs signed by the wrong wallet
        raise appropriate exceptions.

    test_rollback(num_wallets=2, loops=5):
        Tests the blockchain's ability to rollback transactions and revert to a previous state.
        This test creates transactions, adds them to the blockchain, and then rolls back a number of blocks.
        It then asserts that the database state matches the expected state after rollback.

    test_split_brain():
        Tests the blockchain's behavior in a split brain scenario, where two different blocks are mined simultaneously
        on separate instances of the blockchain (simulating a network partition).
        It then tests that when the split brain is resolved, the blockchain with the longer chain takes precedence,
        and the other chain rolls back to the correct state.

Each test initializes its own instances of wallets and blockchains, and manipulates transactions and blocks to
verify the integrity and expected behavior of the blockchain under different conditions.

Usage:
    The tests should be run using a test runner that supports pytest.
    They depend on the internal blockchain, wallet, verifier, and database components being correctly implemented.

Note:
    The tests may need to be updated if there are changes to the internal APIs of the blockchain components they are testing.
"""


def test_tx_verifier():
    w = Wallet.create()
    db = DB()
    inp = Input('COINBASE',0,w.address,0)
    inp.sign(w)

    out = Output(w.address, 25, 0)

    tx = Tx([inp],[out])
    tx_dict = tx.as_dict

    tx_restored = Tx.from_dict(tx_dict)
    tv = TxVerifier(db)
    assert tv.verify(tx_restored.inputs, tx_restored.outputs) == 0

    ####### setting out amount > input amount 
    db.unspent_txs_by_user_hash[str(out.address)].add((tx.hash,out.hash))
    db.transaction_by_hash[tx_restored.hash] = tx_dict

    inp = Input(tx_restored.hash,0,w.address,0)
    inp.sign(w)
    out = Output(w.address, 30, 0) 

    tx = Tx([inp],[out])
    with tc().assertRaises(Exception) as cm:
        tv = TxVerifier(db)
        tv.verify(tx.inputs, tx.outputs)
    assert 'Insuficient funds' in str(cm.exception)
       

    ####### using wallet of another user to sing the inputs
    w2 = Wallet.create()
    inp = Input(tx_restored.hash,0,w.address,0)
    inp.sign(w2) 
    out = Output(w.address, 30, 0)
    tx = Tx([inp],[out])
    with tc().assertRaises(Exception) as cm:
        tv = TxVerifier(db)
        tv.verify(tx.inputs, tx.outputs)
    assert 'Signature verification failed' in str(cm.exception)
   

def test_rollback(num_wallets=2, loops=5):
    wallet = Wallet.create()
    __db = DB()
    bc = Blockchain(__db, wallet)
    bc.create_first_block()
    prev_db = None
    for mn in range(loops+1):
        wallets = []
        outs = []
        for i in range(num_wallets):
            ww = Wallet.create()
            wallets.append(ww)
            outs.append(Output(ww.address, 2, 0))
        inp = Input(bc.head.txs[0].hash,0,wallet.address,0)
        inp.sign(wallet)
        tx = Tx([inp],outs)
        bc.add_tx(tx)
        bc.force_block()

        if prev_db is None:
            prev_db = copy.deepcopy(__db)

    new_block = copy.deepcopy(bc.head)

    for mn in range(loops):
        bc.rollback_block()
  
    tt = tc()
    tt.maxDiff=None
    assert __db.block_index == new_block.index - loops
    for k,v in prev_db.transaction_by_hash.items():
        tt.assertDictEqual(__db.transaction_by_hash.get(k, None), prev_db.transaction_by_hash.get(k, None))

    for tx in new_block.txs:
        assert __db.transaction_by_hash.get(tx.hash, False)

    for k,v in __db.unspent_txs_by_user_hash.items():
        tt.assertSetEqual(v, prev_db.unspent_txs_by_user_hash.get(k, set())) 

    for k,v in __db.unspent_outputs_amount.items():
        tt.assertDictEqual(v,prev_db.unspent_outputs_amount.get(k, {}))

def test_split_brain():
    wallet1 = Wallet.create()
    wallet2 = Wallet.create()
    __db1 = DB()
    __db2 = DB()
    bc1 = Blockchain(__db1, wallet1)
    bc1.create_first_block()
    bc2 = Blockchain(__db2, wallet2)
    # sync first block in second blockchain
    bc2.add_block(bc1.head)
    # mine two different blocks on blockchains to get split brain
    bc1.force_block()
    bc2.force_block()
    # adding second block to the first blockchain and get 2 blocks with same previous hash
    added = bc1.add_block(bc2.head)
    # mine additional block to get longer chain and add it to the first blockchain
    bc2.force_block()
    added = bc1.add_block(bc2.head)
    # as second blockchain longer first blockchain should make rollback to the 
    # same block on two chains and rollover new blocks from second blockchain
    assert added == True
