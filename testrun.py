import requests
import time

# Assuming these are needed for other parts of your script
from blockchain.wallet import Wallet
from blockchain.blocks import Input, Output, Tx

pis = [('192.168.20.2', 8000),('192.168.20.4',8001),('192.168.20.3',8002),('192.168.29.239',8004)]

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
