
from web3 import Web3
import requests
# Initialize Web3 connection using the Infura URL from config file
# infura_url = config['web3']['infura_url']
infura_url = 'https://app.decentdao.org/home?dao=eth:0x36bD3044ab68f600f6d3e081056F34f2a58432c4'
w3 = Web3(Web3.HTTPProvider(infura_url))
# logging.info("Web3 connection initialized")

# Etherscan API URL and event monitoring contract address from config
tryme = '0x111fda21d67e2e3af89d79a78652b89b9ebc418c'
etherscan_api_url = f"https://api-goerli.etherscan.io/api?module=contract&action=getabi&address={tryme}&format=raw"
# https://api-goerli.etherscan.io/api?module=contract&action=getabi&address=0x111fda21d67e2e3af89d79a78652b89b9ebc418c&format=raw
# https://api-goerli.etherscan.io/api?module=contract&action=getabi&address=0xc18360217d8f7ab5e7c516566761ea12ce7f9d72&format=raw
# Fetch the ABI
# response = requests.get(etherscan_api_url)
# if response.status_code == 200:
#     dao_contract_abi = response.text
#     print(dao_contract_abi)
    
def tally_req(url='https://www.tally.xyz/gov/arbitrum/proposals'):
  response = requests.post(url=url)#json={"query": body}
  html_res = response.content.decode('utf8')
  print(html_res)
tally_req()