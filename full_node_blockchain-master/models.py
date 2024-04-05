
from typing import List
from pydantic import BaseModel, Field

"""
Just some Input models for FastApi
"""

"""
Defines Pydantic models to validate and structure data for various blockchain components for use in FastAPI.

Models:
    InputModel:
        Represents an input in a blockchain transaction, containing references to previous transactions,
        output indexes, the associated address, a signature index, and a cryptographic signature.

    OutputModel:
        Represents an output in a blockchain transaction, detailing the amount to be transferred,
        the recipient's address, an index, and the input hash that this output corresponds to.

    TxModel:
        Represents a complete transaction in the blockchain, containing lists of input and output models,
        and a timestamp indicating when the transaction was created.

    BlockModel:
        Represents an individual block in the blockchain, containing the block index, nonce for proof-of-work,
        timestamp, previous block's hash, and a list of transactions (TxModel) contained in the block.

    BlocksModel:
        Represents a list of blocks, serving as a collection that can be used to transmit multiple blocks,
        for example, when syncing the blockchain across nodes.

    NodesModel:
        Represents a list of node identifiers, typically used to manage and update the network's peer information.

Configuration:
    Each model includes a Config class that allows for arbitrary types, which is necessary because blockchain
    data structures often include custom types not natively supported by Pydantic.

Usage:
    These models are used by FastAPI routes to automatically validate and serialize request and response data.
    They enforce a schema on the data being processed by the blockchain's API endpoints.

Note:
    The models are tightly coupled with the blockchain's data structures. If the blockchain implementation changes,
    corresponding updates to these models may be required.
"""



class InputModel(BaseModel):
    prev_tx_hash:str
    output_index:int
    address:str
    index:int
    signature:str

class OutputModel(BaseModel):
    amount:int
    address:str
    index:int
    input_hash:str

class TxModel(BaseModel):
    inputs:List[InputModel]
    outputs:List[OutputModel]
    timestamp:int
    class Config:
        arbitrary_types_allowed = True

class BlockModel(BaseModel):
    index:int
    nonce:int
    timestamp:int
    prev_hash:str
    txs:List[TxModel]
    class Config:
        arbitrary_types_allowed = True

class BlocksModel(BaseModel):
    blocks:List[BlockModel]
    class Config:
        arbitrary_types_allowed = True

class NodesModel(BaseModel):
    nodes:List[str]