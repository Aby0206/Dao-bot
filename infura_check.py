import os  
from dotenv import load_dotenv  
from web3 import Web3, exceptions  
  
load_dotenv()  
# 9c292ef64aeb41f1b234cebccb9a6597
# SyfkjAptGkxSbM6J4/5TqvbVAXWFANWc9Ww/cAcan8ejcxmc3XHufA
  
infura_url = 'https://sepolia.infura.io/v3/<API-KEY>'  
private_key = os.getenv('9c292ef64aeb41f1b234cebccb9a6597')  
# from_account = '<PUBLIC-KEY>'  
# to_account = '<RECIPIENT-PUBLIC-KEY>'  
web3 = Web3(Web3.HTTPProvider(infura_url))  
  
# try:  
#     from_account = web3.to_checksum_address(from_account)  
# except exceptions.InvalidAddress:  
#     print(f"Invalid 'from_account' address: {from_account}")  
  
# try:  
#     to_account = web3.to_checksum_address(to_account)  
# except exceptions.InvalidAddress:  
#     print(f"Invalid 'to_account' address: {to_account}")  
  
# nonce = web3.eth.get_transaction_count(from_account)  
tx = {
    'type': '0x2',
    # 'nonce': nonce,
    # 'from': from_account,
    # 'to': to_account,
    'value': web3.to_wei(0.01, 'ether'),
    'maxFeePerGas': web3.to_wei('250', 'gwei'),
    'maxPriorityFeePerGas': web3.to_wei('3', 'gwei'),
    'chainId': 11155111
}
gas = web3.eth.estimate_gas(tx)
tx['gas'] = gas
signed_tx = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("Transaction hash: " + str(web3.to_hex(tx_hash)))