from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import json
from datetime import datetime
import os
from typing import Final
import asyncio

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


sendAtTime = {}
# from responses import sendAt
warning_hours: Final[str] = os.getenv('DISCORD_WARNING_HOURS')
# future_send = sendAt(proposal['end']-int(warning_hours)*60*60,output)
def sendAt(timestamp,output):
  print(f'timestamp: {timestamp} {type(timestamp)}')
  dt_object = datetime.fromtimestamp(float(timestamp))
  print(dt_object)
  sendAtTime[dt_object] = output
  return sendAtTime

async def getTallyInner(inner_coin = '/gov/arbitrum/proposal/',proposal_headding=''):
    # Set up options to run Chrome in headless mode (without GUI)
    global date_proposal
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Set up the webdriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Define the URL
    url = f'https://www.tally.xyz'+inner_coin
    # print(f'url: {url}')
    # Open the URL
    driver.get(url)
    # Wait for the entire page to load (adjust the time as needed)
    # time.sleep(10)
    await asyncio.sleep(10)

    # chakra-card css-vutloh
    tables = driver.find_elements(By.CLASS_NAME, 'chakra-card__body')
    for table in tables:
        rows = table.find_elements(By.TAG_NAME, 'p')
        counter_inner = -1
        for row in rows:
            if 'Voting period started' in row.get_attribute('outerHTML'):
                counter_inner = 0
            if counter_inner>=0:
                counter_inner += 1
            if counter_inner == 4:
                date_str = row.get_attribute('outerHTML').split('>')[1].replace('</p', '')
                print(f'check data {coin} '+date_str)
                
                current_year = datetime.now().year

                # Convert to datetime object with the current year
                dt_object = datetime.strptime(f"{current_year} {date_str}", "%Y %a %b %d, %I:%M %p")
                print(f'dt_object {dt_object}')
                # Convert to timestamp
                timestamp = dt_object.timestamp()
                cacheIds_var = cacheIds('','r')
                the_key = f'{proposal_headding} {url} {str(timestamp)}'
                if the_key+'\n' not in cacheIds_var:
                    date_proposal[f'{proposal_headding} {url}'] = timestamp
                    cacheIds_var = cacheIds(the_key,'w')
                else:
                    print(f'skipping {the_key}')
                    
                print(date_proposal)
                # if coin not in date_coins:
                #     date_coins[coin] = [timestamp]
                # else:
                #     date_coins[coin].append(timestamp)
    # tables = driver.find_elements(By.CLASS_NAME, 'proposal-description')
    # for table in tables:
    #     rows = table.find_elements(By.TAG_NAME, 'p')
    #     for row in rows:
    #         print(row.get_attribute('outerHTML'))
    # print(f'url: {url}')
async def getBoardroom(coin = 'arbitrum'):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Set up the webdriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Define the URL
    url = f'https://www.tally.xyz/gov/{coin}/proposals'
    url = f'https://boardroom.io/{coin}/proposals'
    url = 'https://boardroom.io/aave/proposal/cHJvcG9zYWw6YWF2ZTpzbmFwc2hvdDoweGY4N2NmMDc2MWIyN2JlY2Y2YzhkMThiYmI0NTdjOWU2YmY2YjdhYTQzNmNkYjBkMTk3YWQyZDkzYTQ5NWVkMDQ='
    # print(f'url: {url}')
    # Open the URL
    # Open the URL
    driver.get(url)
    await asyncio.sleep(10)
    # Wait for the element to be present in the DOM
    try:
        # Explicit wait to ensure the element is loaded
        wait = WebDriverWait(driver, 10)
        
        # Switch to iframe if necessary (uncomment and update the selector if your element is within an iframe)
        # iframe = wait.until(EC.presence_of_element_located((By.XPATH, "your_iframe_xpath")))
        # driver.switch_to.frame(iframe)

        # Wait until the specific element is present
        # element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/section/section/div[2]/div/main/div/div[2]/main/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/p')))
        # element = wait.until()
        # Custom condition to wait for at least one <p> element to be present
        elements = wait.until(lambda d: d.find_elements(By.TAG_NAME, 'p'))

        # Iterate through all found <p> elements and print their outer and inner HTML
        for p in elements:
            print(p.get_attribute('outerHTML'))
            print(p.get_attribute('innerHTML'))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the driver
        driver.quit()

async def getTally(coin = 'arbitrum'):
    # Set up options to run Chrome in headless mode (without GUI)
    global date_proposal
    date_proposal = {}
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Set up the webdriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Define the URL
    url = f'https://www.tally.xyz/gov/{coin}/proposals'
    # print(f'url: {url}')
    # Open the URL
    driver.get(url)

    # Wait for the entire page to load (adjust the time as needed)
    # time.sleep(10)
    await asyncio.sleep(10)

    # Find the table element by its class name (chakra-table)
    table = driver.find_element(By.CLASS_NAME, 'chakra-table')

    # Extract table rows
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # Extract table headers
    headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, 'th')]
    headers = ['proposals','votes for','votes against','total votes']
    # Debugging: print headers
    # print("Headers:", headers)

    # Extract table data
    table_data = []
    for row in rows[1:]:
        # skip_row = False
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = []
        # print('row')
        counter_date = 0
        
        for cell in cells:
            # Find all <p> tags within the cell
            p_tags = cell.find_elements(By.TAG_NAME, 'p')
            span_tags = cell.find_elements(By.TAG_NAME, 'span')
            a_tags = cell.find_elements(By.TAG_NAME, 'a')
            span_val = ''
            for span_tg in span_tags:
                span_val = span_tg.get_attribute('outerHTML').split('>')[1].replace('</span', '')
            if span_val == 'Executed' or span_val == 'Canceled':
                # print(f'span_tg : {span_val}')
                # skip_row = True
                break
            for a_tag in a_tags:
                a_value = a_tag.get_attribute('outerHTML').split('href=')[1].split('>')[0]
                proposal_headding = a_tag.get_attribute('innerHTML').split('>')[1].replace('</p', '')
                print('innerHTML '+proposal_headding)
                
                # print(f'a_value: {a_value}\n{a_tag.get_attribute('outerHTML')}')
                await getTallyInner(a_value.replace('"', ''),f'{coin} {proposal_headding}')
                
            text = ''
            # Debugging: print each <p> tag's HTML
            for p in p_tags:
                # print(counter_date)
                counter_date+=1
                # print("P Tag HTML:", p.get_attribute('outerHTML'))
                if counter_date == 2:
                    pass
                    # print(p.get_attribute('outerHTML').split('>')[1].replace('</p', ''))
                    
                text += p.get_attribute('outerHTML').split('>')[1].replace('</p', '')+' '
            
            # # Extract text from each <p> tag
            # text = " ".join([p.text.strip() for p in p_tags])
            
            row_data.append(text)
            
            # For debugging: show extracted text
            # print("Extracted Text:", text)
            
        table_data.append(row_data)
    print(f'date_proposal {date_proposal}')
    output = ''
    futureSend = {}
    for key in date_proposal:
        output += key
        futureSend = sendAt(str(date_proposal[key]),key)
    if output == '':
        output = 'no new proposals'
    print(f'output,futureSend {output} {futureSend}')
    return output,futureSend
    # Convert to DataFrame
    df = pd.DataFrame(table_data, columns=headers)
    # print(df['proposals'])
    df.to_csv(f'./tally_Result/{coin}.csv')
    # Close the browser
    driver.quit()
    print('\n'.join(list(df['proposals']))+'\n-----------')
    return ('\n'.join(list(df['proposals']))+'\n-----------','')
# getTally()
# # allcoins_str = '".eth",".eth",".eth",".eth",".eth",".eth",".eth",".eth","staging.daoplomats.eth" '
# # allcoins = [coin.split('.')[0].replace('"', '') for coin in allcoins_str.split(',')]
allcoins = ['aave','ens','gmx','arbitrum']
allcoins = ['aave']
failed_coins = {}
date_coins = {}
date_proposal = {}
for coin in allcoins:
    try:
        asyncio.run(getBoardroom(coin))
        print(f'coin: {coin}')
    except Exception as e:
        print(f'failed coin: {coin} \n{e}')
        failed_coins[coin] = e
# print(failed_coins)
# print(date_coins)
# print(date_proposal)
# for failed in failed_coins.keys():
#     # Define the URL
#     url = f'https://www.tally.xyz/gov/{failed}/proposals'
#     print(f'failed url: {url}')