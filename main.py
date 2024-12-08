# bot.py
import os

import discord
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
async def start_game(interation: discord.Interaction):
    await interation.response.send_message(
        f"Game of Garlic Tone started!"
    )

#@client.event
#async def on_ready():
#    print(f'{client.user} has connected to Discord!')

@client.event
async def on_ready():  #  Called when internal cache is loaded
    #channel = discord.utils.get(client.get_all_channels(), name=name_channel)
    channel_id =1315251666349588492
    channel = client.get_channel(channel_id) #  Gets channel from internal cache
    await channel.send("hello world") #  Sends message to channel




client.run(TOKEN)
