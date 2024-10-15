from random import choice, randint
import requests
import json
import datetime
import os
from typing import Final
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from runtally import getTally
import asyncio
load_dotenv()
BOARDROOM_KEY: Final[str] = os.getenv('BOARDROOM_KEY')

def parse_html_response(html_response):
    soup = BeautifulSoup(html_response, 'html.parser')
    title = soup.title.string  # Get the title of the page
    # print(f'title {title}')
    print(soup)
    if title == "Page Not Found":
        # If the title is "Page Not Found", store the URL as bad.
        bad_url = True
    else:
        bad_url = False
    return bad_url

load_dotenv()

allcoins_str = '"aave.eth","ens.eth","safe.eth","arbitrumfoundation.eth","shutterdao0x36.eth","uniswapgovernance.eth","gmx.eth","gitcoindao.eth","staging.daoplomats.eth" '
allcoins = allcoins_str.split(',')
urls = {
  'aave.eth':'https://app.fractalframework.xyz/home?dao=eth:0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9',
  "ens.eth":'https://app.fractalframework.xyz/home?dao=eth:0xc18360217d8f7ab5e7c516566761ea12ce7f9d72',
  "safe.eth":'https://app.fractalframework.xyz/home?dao=eth:0x5afe3855358e112b5647b952709e6165e1c1eeee',
  "arbitrumfoundation.eth":'https://app.fractalframework.xyz/home?dao=eth:0xB50721BCf8d664c30412Cfbc6cf7a15145234ad1',
  "shutterdao0x36.eth":'https://app.fractalframework.xyz/home?dao=eth:0x36bD3044ab68f600f6d3e081056F34f2a58432c4',
  "uniswapgovernance.eth":'https://app.fractalframework.xyz/home?dao=eth:0x1f9840a85d5af5bf1d1762f925bdaddc4201f984',
  "gmx.eth":'https://app.fractalframework.xyz/home?dao=eth:0x1bc08b2e6537166ad57c2dd1ab27241fea9a14cb',
  "gitcoindao.eth":'https://app.fractalframework.xyz/home?dao=eth:0xde30da39c46104798bb5aa3fe8b9e0e1f348163f',
  # "staging.daoplomats.eth" :'https://app.fractalframework.xyz/home?dao=eth:'
  
  }
sendAtTime = {}
SNAPSHOT_API_URL = "https://api.snapshot.org/graphql"
warning_hours: Final[str] = os.getenv('DISCORD_WARNING_HOURS')


def writeCacheIds(ids):
  file1 = open('idcache.txt',"a")
  file1.write(ids+'\n')
  file1.close()
  return readCacheIds()
  
def readCacheIds():
  try:
    file1 = open('idcache.txt',"r")
    output = []
    for x in file1:
      output.append(x)
    # print(output)
    return output
  except:
    writeCacheIds('')

def cacheIds(ids,rw):
  if rw =='r':
    return readCacheIds()
  if rw =='w':
    return writeCacheIds(ids)
  
  

def sendAt(timestamp,output):
  dt_object = datetime.datetime.fromtimestamp(int(timestamp))
  print(f'dt_object {dt_object} {timestamp} {output}')
  # exit()
  sendAtTime[dt_object] = output
  return sendAtTime

from concurrent.futures import ThreadPoolExecutor
def getAll_protocol():
  url = f'https://api.boardroom.info/v1/protocols?key={BOARDROOM_KEY}'
  response = requests.get(url=url)#json={"query": body}
  response_json = response.json()
  protocols = []
  if 'data' in response_json and isinstance(response_json['data'], list):
    for protocol in response_json['data']:
      protocols.append(protocol['cname'])
  print(f'protocols {protocols}')
  the_out = []
  for each_protocol in protocols:
    the_out.append(req_boardroom(each_protocol))
  return the_out
def req_boardroom(protocal):
    print(f'req_boardroom {protocal} {BOARDROOM_KEY}')
    url = f'https://api.boardroom.info/v1/protocols/{protocal}/proposals?key={BOARDROOM_KEY}'
    print(url)
    response = requests.get(url=url)#json={"query": body}
    date_proposal = {}
    checkIds = cacheIds('','r')
    # Parse the response JSON
    response_json = response.json()
    # Debug: Print the entire JSON response to understand its structure
    # print(response_json)
    nothing_viewed = True
    output = ''
    # Check if 'data' is in the response and is a list
    if 'data' in response_json and isinstance(response_json['data'], list):
        # Iterate over each proposal in the data list
        for proposal in response_json['data']:
            # Access the 'id' field of each proposal
            if proposal['currentState'] not in ['closed','canceled','executed']:
              eachOut = ''
              if f"{proposal['id']} {proposal['refId']}\n" in checkIds:
                continue
              nothing_viewed = False
              if 'id' in proposal:
                print('id '+proposal['id'])
              if 'refId' in proposal:
                print('refId '+proposal['refId'])
              if 'protocol' in proposal:
                print('protocol '+proposal['protocol'])
              if 'currentState' in proposal:
                print('currentState '+proposal['currentState'])
              if 'title' in proposal:
                print('title '+proposal['title'])
                eachOut += proposal['title']+'\n'
              if 'externalUrl' in proposal:
                print('externalUrl '+proposal['externalUrl'])
                eachOut += proposal['title']+'\n'
              if 'endTimestamp' in proposal:
                print('endTimestamp '+proposal['endTimestamp'])
              eachOut += f'https://boardroom.io/{proposal['protocol']}/proposal/{proposal['refId']}\n'
              output+=eachOut
              date_proposal[f'{proposal['id']} {proposal['refId']}\n{eachOut}'] = int(proposal['endTimestamp'])-int(warning_hours)*60*60
              cacheIds(f"{proposal['id']} {proposal['refId']}",'w')
    else:
        print("No data found in the response.")
    if nothing_viewed==True:
      print(f'nothing_viewed {url}')
    futureSend = {}
    for key in date_proposal:
        output += key
        futureSend = sendAt(str(date_proposal[key]),key)
    if output == '':
        output = 'no new proposals'
    print(f'output,futureSend {output} {futureSend}')
    return output,futureSend
async def req_snapshot(check=None):
  if check is None or check == 'snapshot':
    return req_snapshot_snapshot()
  if 'fractal' in check:
    return req_snapshot_fractal(check.split(':')[1])
  if 'tally' in check:
      # loop = asyncio.get_event_loop()
      # with ThreadPoolExecutor() as pool:
      #     result = await loop.run_in_executor(pool, getTally, check.split(':')[1])
      #     return result
    return await getTally(check.split(':')[1])
  if 'boardroom' in check:
    if check.split(':')[1] == '*':
      return getAll_protocol()
        
    else:
      return req_boardroom(check.split(':')[1])

def req_snapshot_fractal(coin):
  url = urls[coin]
  print(coin)
  print(url)
  response = requests.post(url=url)#json={"query": body}
  html_res = response.content.decode('utf8')
  print(url)
  print(parse_html_response(html_res))
  # my_json = json.loads(my_json)
          
  return 'fractal',''

def req_snapshot_snapshot():
  # we have imported the requests module
          #import requests
          # defined a URL variable that we will be
          # using to send GET or POST requests to the API
          url = "https://hub.snapshot.org/graphql"
          # aave.eth
          # ens.eth
          # safe.eth
          # arbitrumfoundation.eth
          # shutterdao0x36.eth
          # uniswapgovernance.eth
          # gmx.eth
          # gitcoindao.eth
          body = """
          query Proposals {
            proposals(
              first: 1000,
              skip: 0,
              where: {
                space_in: [ """+allcoins_str+"""],
                state: "active"
              },
              orderBy: "created",
              orderDirection: desc
            ) {
              id
              title
              body
              choices
              start
              end
              snapshot
              state
              author
              space {
                id
                name
              }
            }
          }
          """


          response = requests.post(url=url, json={"query": body})
          my_json = response.content.decode('utf8')
          my_json = json.loads(my_json)
          future_send = ''
          if response.status_code == 200:
              output = ''
              checkIds = cacheIds('','r')
              for proposal in my_json['data']["proposals"]:
                if proposal['id']+'\n' in checkIds:
                  continue
                #proposal['space']['name']+'\n'+proposal['snapshot']+'\n'
                output+=proposal['title']+'\n'+f'https://snapshot.org/#/{proposal['space']['id']}/proposal/{proposal['id']}\n'
                if proposal['end']!=None:
                  print('::::::::::::::::')
                  print(proposal['end']-int(warning_hours)*60*60)
                  print(output)
                  future_send = sendAt(proposal['end']-int(warning_hours)*60*60,output)
                cacheIds(proposal['id'],'w')
              checkIds = cacheIds('','r')
              if output !='':
                return output,future_send
              else:
                return 'no new proposals',future_send
          else:
              return "bad request",future_send
          
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'bad, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1, 6)}'

    elif 'p' in lowered:
        out1,out2 = req_snapshot()
        return out1

    else:
        return choice(['I dont understand...',
                       'What are u talking about',
                       'Do you mind rephracing that?'])