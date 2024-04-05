import requests
import time

# Assuming these are needed for other parts of your script
from blockchain.wallet import Wallet
from blockchain.blocks import Input, Output, Tx

"""
Periodically queries the status of multiple blockchain nodes in a network and prints out their latest block information.

This script continuously makes HTTP GET requests to the '/chain/status' endpoint of each node in the network.
It then prints out the current index, timestamp, previous hash, and block hash for the latest block in each node's blockchain.
If the request fails or a node is unreachable, it logs an error message.

Variables:
    pis (list of tuple): A list of tuples containing IP addresses and ports of the blockchain nodes.

Loop:
    The script enters an infinite loop, where it iterates through each node specified in 'pis'.
    For each node, it attempts to:
        - Query the node's status.
        - Parse the JSON response.
        - Print the relevant block information.
    If the node is not reachable or any other error occurs during the request, it catches the exception and prints an error message.
    After iterating through all nodes, it prints a separator line and sleeps for 2 seconds before repeating the process.

Usage:
    This script is useful for monitoring the status and consistency of a blockchain network by periodically checking the status of each node.
    It could be used in a dashboard, monitoring system, or for troubleshooting purposes during development and testing.

Note:
    This script assumes that the '/chain/status' endpoint returns a JSON object with specific fields. Any changes to the node's API could require updates to the script.
"""


pis = [('192.168.20.2', 8000),('192.168.20.4',8001),('192.168.20.3',8002),('192.168.20.5', 8003), ('192.168.20.6',8004)]

while True:
    for ip, port in pis:
        try:
            response = requests.get(f"http://{ip}:{port}/chain/status").json()
            # Extracting the additional information
            block_hash = response.get('block_hash')
            timestamp = response.get('timestamp')
            #index = response.get('index')
            #prev_hash = response.get('prev_hash')
            index = response.get('block_index')
            prev_hash = response.get('block_prev_hash')
            
            print(f"IP: {ip}:{port} | Index: {index} | Timestamp: {timestamp} | Previous Hash: {prev_hash} | Block Hash: {block_hash}")
        except Exception as e:
            print(f"Failed to retrieve data from {ip}:{port}. Error: {e}")
    print('===============================================================')
    time.sleep(2)
