# bot.py
import os
import asyncio
import discord
import re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

TEST_SERVER = discord.Object(id=1315251665674440714)

#client = discord.Client(intents=discord.Intents.default())

class MyClient(discord.Client):
    def __init__(self):
        intents_list = discord.Intents.default()
        #intents_list.message_content = True
        super().__init__(intents=intents_list)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=TEST_SERVER)
        await self.tree.sync(guild=TEST_SERVER)

client = MyClient()

@client.tree.command(description="Start A Game Of Garlic Tone With The Bot")
async def start_game(interaction: discord.Interaction):
    channel_id = 1315251666349588492
    channel = client.get_channel(channel_id)
    players = []
    await interaction.response.send_message(
        f"Game of Garlic Tone started!"
    )
    channel_id =1315251666349588492
    channel = client.get_channel(channel_id) #  Gets channel from internal cache
    await channel.send("hello world") #  Sends message to channel
    players = []

    message = await channel.send(
        f"React to this message with ✅ to join the game!"
    )
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

#@client.event
#async def on_ready():
#    print(f'{client.user} has connected to Discord!')

@client.event
async def on_ready():  #  Called when internal cache is loaded
    #channel = discord.utils.get(client.get_all_channels(), name=name_channel)
    pass

@client.event
async def send_dm_to_players(players):
    for player in players:
        player = player[2:]
        player = player[:-1]
        print(player)
        user = await client.fetch_user(player)
        await user.send(file=discord.File('blankdrawing.png'))
    await asyncio.sleep(20)
    await download_image_and_send(players)

@client.event
async def download_image_and_send(players):
    os.mkdir('temp')
    for player in players:
        player = player[2:]
        player = player[:-1]
        user = await client.fetch_user(player)
        if user:
            # found the user
            messages = [message async for message in user.history(limit=1)]
            latestmessage = messages[0]
            if not latestmessage.attachments: # Checks if there is an attachment on the message
                print("Balls")
                return
            else: # If there is it gets the filename from message.attachments
                imageName = "temp/image" + player + ".png"
                await latestmessage.attachments[0].save(imageName) # saves the file
                print("wins")
        else:
            # Not found the user
            print("Fuck")



@client.tree.command(description="Joins VC")
async def joinvc(interaction: discord.Interaction):
    channel = interaction.user.voice.voice_channel
    await client.join_voice_channel(channel)



client.run(TOKEN)
