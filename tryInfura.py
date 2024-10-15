# url = 'https://arbitrum-mainnet.infura.io/v3/9c292ef64aeb41f1b234cebccb9a6597'
# url = 'https://arbitrum-mainnet.infura.io/v3/9c292ef64aeb41f1b234cebccb9a6597'
# url = 'https://sepolia.infura.io/v3/9c292ef64aeb41f1b234cebccb9a6597'  

# 9c292ef64aeb41f1b234cebccb9a6597
# SyfkjAptGkxSbM6J4/5TqvbVAXWFANWc9Ww/cAcan8ejcxmc3XHufA

# https://mainnet.infura.io/v3/9c292ef64aeb41f1b234cebccb9a6597
# curl -X POST -u "<API_KEY>:<API_KEY_SECRET>" 
# url = "https://ipfs.infura.io:5001/api/v0/cat?arg=QmeGAVddnBSnKc1DLE7DLV9uuTqo5F7QbaveTjr45JUdQn"
# url = 'https://arbitrum-mainnet.infura.io/v3/9c292ef64aeb41f1b234cebccb9a6597'
# 'https://base-mainnet.infura.io/v3/YOUR-API-KEY'
# 'https://polygon-mainnet.infura.io/v3/YOUR-API-KEY'


import requests
import json
API_KEY = '9c292ef64aeb41f1b234cebccb9a6597'

# def hexval(hex_val = '0x00000000219ab540356cBB839Cbe05303d7705Fa'):
#     return str(int(hex_val.split('0x')[1],16))
# print(hexval())

def sendReqEther(url):
    
    # headers = {'content-type': 'application/json'}
    response = requests.get(url)#.json()
    return response.text
def sendReqInfura(url = 'https://mainnet.infura.io/v3/',infura_method="eth_blockNumber",params=[]):
    

    payload = {
        "jsonrpc": "2.0",
        "method": infura_method,
        "params": params,
        "id": 1
    }

    headers = {'content-type': 'application/json'}

    response = requests.post(url+API_KEY, data=json.dumps(payload), headers=headers)#.json()

    return response
def block_num(url,infura_method,params):
    # curl https://mainnet.infura.io/v3/YOUR-API-KEY \
    #     -X POST \
    #     -H "Content-Type: application/json" \
    #     --data '{"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber", "params": []}'
    response = sendReqInfura(url,infura_method,params)

    i = int(json.loads(response.text)['result'].split('0x')[1], 16)
    print(f'{the_coin} block_num: {str(i)}')
def wei_data(url,infura_method,params):
    # curl https://mainnet.infura.io/v3/API-KEY \
    #     -X POST \
    #     -H "Content-Type: application/json" \
    #     -d '{"jsonrpc":"2.0","method":"eth_getBalance","params": ["0x00000000219ab540356cBB839Cbe05303d7705Fa", "latest"],"id":1}'
    infura_method = 'eth_getBalance'
    params=["0x00000000219ab540356cBB839Cbe05303d7705Fa", "latest"]
    response = sendReqInfura(url,infura_method,params)
    i = int(json.loads(response.text)['result'].split('0x')[1], 16)
    print(f'{the_coin} Wei: {str(i)}')


the_coin = 'mainnet'
url = f'https://{the_coin}.infura.io/v3/'
infura_method="eth_blockNumber"
params=[]

the_coins = ['mainnet','arbitrum-sepolia']

# for the_coin in the_coins:
#     print(sendReqInfura(url,infura_method,params).text)
#     block_num(url,infura_method,params)
#     wei_data(url,infura_method,params)
    
# print(sendReqEther('https://etherscan.io/token/0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9'))
ethids = [
'0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9',
'0xc18360217d8f7ab5e7c516566761ea12ce7f9d72',
'0x5afe3855358e112b5647b952709e6165e1c1eeee',
'0xB50721BCf8d664c30412Cfbc6cf7a15145234ad1',
'0x36bD3044ab68f600f6d3e081056F34f2a58432c4',
'0x1f9840a85d5af5bf1d1762f925bdaddc4201f984',
'0x1bc08b2e6537166ad57c2dd1ab27241fea9a14cb',
'0xde30da39c46104798bb5aa3fe8b9e0e1f348163f',

https://app.fractalframework.xyz/daos/0x0348B55AbD6E1A99C6EBC972A6A4582Ec0bcEb5c/proposals
]
for eath in ethids:
    print(sendReqEther(f'https://app.fractalframework.xyz/daos/{eath}/proposals'))
    break
https://app.fractalframework.xyz/home?dao=eth:0x0348B55AbD6E1A99C6EBC972A6A4582Ec0bcEb5c
'https://app.fractalframework.xyz/home?dao=eth:0x36bD3044ab68f600f6d3e081056F34f2a58432c4'
'https://app.fractalframework.xyz/daos/0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9/proposals',
'https://app.fractalframework.xyz/daos/0xc18360217d8f7ab5e7c516566761ea12ce7f9d72/proposals',
'https://app.fractalframework.xyz/daos/0x5afe3855358e112b5647b952709e6165e1c1eeee/proposals',
'https://app.fractalframework.xyz/daos/0xB50721BCf8d664c30412Cfbc6cf7a15145234ad1/proposals',
'https://app.fractalframework.xyz/daos/0x36bD3044ab68f600f6d3e081056F34f2a58432c4/proposals',
'https://app.fractalframework.xyz/daos/0x1f9840a85d5af5bf1d1762f925bdaddc4201f984/proposals',
'https://app.fractalframework.xyz/daos/0x1bc08b2e6537166ad57c2dd1ab27241fea9a14cb/proposals',
'https://app.fractalframework.xyz/daos/0xde30da39c46104798bb5aa3fe8b9e0e1f348163f/proposals',
https://app.fractalframework.xyz/daos//proposals
