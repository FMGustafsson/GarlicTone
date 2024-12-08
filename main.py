# bot.py
import os
import asyncio
import discord
import re
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
    players = []

    message = await channel.send("Message")
    await message.add_reaction('✅')
    await asyncio.sleep(10)

    message = await channel.fetch_message(message.id)

    for reaction in message.reactions:
        print("yeet")
        if reaction.emoji == '✅':
            async for user in reaction.users():
                if user != client.user:
                    players.append(user.mention)

    if len(players) < 1:
        await channel.send('Time is up, and not enough players')
    else:
        print(players[0])

        await channel.send(players)
    
    await send_dm_to_players(players)

@client.event
async def send_dm_to_players(players):
    blank = open("blankdrawing.png", "r")
    for player in players:
        player = player[2:]
        player = player[:-1]
        print(player)
        user = await client.fetch_user(player)
        await user.send(file=discord.File('blankdrawing.png'))


client.run(TOKEN)
