# main.py
            
import asyncio
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response,req_snapshot
import time
from discord.ext import tasks
from datetime import datetime, timedelta

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL: Final[str] = os.getenv('DISCORD_WEBHOOK_URL')  # Add this to your .env file
time_sleep_seconds: Final[str] = os.getenv('DISCORD_TIME')
warning_hours: Final[str] = os.getenv('DISCORD_WARNING_HOURS')
BOARDROOM_KEY: Final[str] = os.getenv('BOARDROOM_KEY')
print(f'BOARDROOM_KEY {BOARDROOM_KEY}')
print(f'warning_hours {warning_hours}')
future_data = {}
print(TOKEN)

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Message Functionality
async def send_message(message: Message, user_message: str) -> None:
    loadcount = 0
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    
    try:
            response: str = get_response(user_message)
            if response == 'no new proposals':
                loadcount+=1
            # time.sleep(loadcount*2)
            await asyncio.sleep(loadcount*2)
            print(message)
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    gen_channel = ''
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.name == 'general':
                gen_channel = channel
                break
    try:
        asyncio.create_task(keep_calling_req(gen_channel))
    except Exception as e:
        print(e)
        file1 = open('errorLog.txt',"a")
        file1.write('Error at '+datetime.now()+'\n'+e+'\n')
        file1.close()


# async def keep_calling_req(gen_channel):
#     global future_data
#     print(future_data)
#     sent_no_proposals = False
#     while True:
#         data_req1 = req_snapshot('fractal')
        
#         data_req,temp_future_data = req_snapshot()
#         if temp_future_data!='':
#             future_data = temp_future_data
        
#         for key in future_data:
#             time_diff = key-datetime.now()
#             if time_diff.total_seconds() < 60:
#                 await gen_channel.send(data_req)
#                 sent_no_proposals = True
#                 del future_data[key]
#             # else:
#             #     print('more 1 min')

#         if data_req == 'no new proposals':
#             if not sent_no_proposals:
#                 await gen_channel.send(data_req)
#                 sent_no_proposals = True
#         else:
#             await gen_channel.send(data_req)
#             sent_no_proposals = False
#         await asyncio.sleep(float(time_sleep_seconds))

        
        
async def keep_calling_req(gen_channel):
    global future_data
    print(f'future_data {future_data}')
    sent_no_proposals = False
    while True:
        # List to hold all data requests
        # future get protocols live url: https://api.boardroom.info/v1/protocols?key=a9e2a08afc04b15bd17e20f05373b9e5
        data_reqs = [
                    # req_snapshot("fractal:aave.eth")
                    # req_snapshot("fractal:aave.eth"),req_snapshot("fractal:ens.eth"),req_snapshot("fractal:safe.eth"),req_snapshot("fractal:arbitrumfoundation.eth"),req_snapshot("fractal:shutterdao0x36.eth"),req_snapshot("fractal:uniswapgovernance.eth"),req_snapshot("fractal:gmx.eth"),req_snapshot("fractal:gitcoindao.eth"),
                    await req_snapshot("tally:aave"),await req_snapshot("tally:arbitrum"),await req_snapshot("tally:ens"),await req_snapshot("tally:gmx"),
                    
                    await req_snapshot("tally:ens"),await req_snapshot("tally:arbitrum"),
                    await req_snapshot(),
                    await req_snapshot("boardroom:aave"),await req_snapshot("boardroom:ens"),await req_snapshot("boardroom:safe"),await req_snapshot("boardroom:arbitrumfoundation"),await req_snapshot("boardroom:shutterdao0x36"),await req_snapshot("boardroom:uniswapgovernance"),await req_snapshot("boardroom:gmx"),await req_snapshot("boardroom:gitcoindao")
                    
                    ]
        # TAKES TOO LONG
        # data_reqs.extend(await req_snapshot('boardroom:*'))
        
        # Add more data requests as needed
        # data_reqs.append(req_snapshot('another_argument'))
        # data_reqs.append(req_snapshot('yet_another_argument'))
        # ...
        await asyncio.sleep(float(60))
        for data_req in data_reqs:
            print(f'data_req {data_req}')
            _, temp_future_data = data_req
            print(f'data_req {data_req}')
            if temp_future_data != '':
                future_data = temp_future_data

        for key in future_data:
            print(f'key {key}')
            time_diff = key-datetime.now()
            if time_diff.total_seconds() < 60:
                # Send all data requests
                for data_req in data_reqs:
                    message, data = data_req
                    if message != 'no new proposals' and data:
                        print(f'data_req future {len(data_req)} \n{data_req}')
                        await gen_channel.send(data_req[0])
                sent_no_proposals = True
                del future_data[key]

        if all(data_req[0] == 'no new proposals' and not data_req[1] for data_req in data_reqs):
            if not sent_no_proposals:
                for data_req in data_reqs:
                    message, data = data_req
                    if message != 'no new proposals' and data:
                        print(f'data_req sent no {len(data_req)} \n{data_req}')
                        await gen_channel.send(data_req[0])
                sent_no_proposals = True
        else:
            for data_req in data_reqs:
                message, data = data_req
                print(f'check {data_req}')
                if message != 'no new proposals' and data:
                    print(f'data_req send {len(data_req)} \n{data_req}')
                    await gen_channel.send(data_req[0])
            sent_no_proposals = False
        print(f'time_sleep_seconds {time_sleep_seconds}')
        await asyncio.sleep(float(time_sleep_seconds))




# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()