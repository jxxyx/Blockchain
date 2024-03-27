import requests
import time

from blockchain.wallet import Wallet
from blockchain.blocks import Input, Output, Tx

pis = [('172.18.4.99', 8000), ()]

while True:
    for ip, port in pis:
        try:
            print(requests.get(f"http://{ip}:{port}/chain/status").json()['block_hash'])
        except:
            pass
    print('===============================================================')
    time.sleep(2)