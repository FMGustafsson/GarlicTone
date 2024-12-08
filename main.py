# bot.py
import os
import asyncio
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

@client.event
async def send_dm(userID, message):
    user = await client.fetch_user(userID)
    await user.send(message)


client.run(TOKEN)
