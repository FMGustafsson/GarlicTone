# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

client = discord.Client(intents=discord.Intents.default())

#@client.event
#async def on_ready():
#    print(f'{client.user} has connected to Discord!')

@client.event
async def on_ready():  #  Called when internal cache is loaded
    #channel = discord.utils.get(client.get_all_channels(), name=name_channel)
    channel_id =1315251666349588492
    channel = client.get_channel(channel_id) #  Gets channel from internal cache
    await channel.send("hello world") #  Sends message to channel
    await send_dm('<@598109867382931476>', "Tom isn't Pog")

@client.event
async def send_dm(userID, message):
    user = await client.fetch_user(userID)
    await user.send(message)

client.run(TOKEN)
