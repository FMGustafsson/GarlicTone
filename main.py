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

class MyClient(discord.Client):
    def __init__(self):
        intents_list = discord.Intents.default()
        super().__init__(intents=intents_list)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=TEST_SERVER)
        await self.tree.sync(guild=TEST_SERVER)

client = MyClient()

@client.tree.command(description="Start a game of garlic tone with the bot")
async def start_game(interaction: discord.Interaction):
    players = []
    message = await interaction.response.send_message(
        f"Game of Garlic Tone started!"
    )
    channel = interaction.channel
    message = await channel.send(
        f"React to this message with ✅ to join the game!"
    )
    await message.add_reaction('✅')
    await asyncio.sleep(10)
    message = await channel.fetch_message(message.id)
    for reaction in message.reactions:
        if reaction.emoji == '✅':
            async for user in reaction.users():
                if user != client.user:
                    players.append(user.mention)
    if len(players) < 1:
        await channel.send("No players have joined!")
    else:
        await channel.send("The following players have joined the game!\n" + str(players))
        for i in range(len(players)):
            players[i] = players[i][2:]
            players[i] = players[i][:-1]
            print(players)
            user = await client.fetch_user(players[i])
            await user.send(file=discord.File('blankdrawing.png'))
        await asyncio.sleep(20)
        await download_image_and_send(players)


@client.tree.command(description="Describe what the bot does")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title = "GarlicTone Information", 
        description = "This is a version of the popular online game 'gartic phone' that runs entirely in discord. Run /start_game to give it a try! Alternatively, run /help to see all the commands you can use.",
        color = 0xff0000
    )
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    embed.add_field(name="Date Made:", value="08/12/2024")
    embed.add_field(name="Team:", value="Crack")
    embed.set_footer(text="Made for the CSS Botathon 2024!")
    await interaction.response.send_message(embed=embed)

@client.tree.command(description="Lists all commands for the bot")
async def help(interaction: discord.Integration):
    embed = discord.Embed(
        title = "GarlicTone Help",
        description = "The help command lists and describes the basics of all commands you can use!",
        color = 0xff0000
    )
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    embed.add_field(name="start_game", value="The 'start_game' command allows you to start a game of GarticTone! Make sure to react to the message to join the game!")
    embed.add_field(name="info", value="The 'info' command displays basic information about the GarlicTone bot, including how to use it.")
    embed.add_field(name="help", value="The 'help' commands displays all the possible commands and what they do.")
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():  #  Called when internal cache is loaded
    pass

@client.event
async def download_image_and_send(players):
    if not os.path.exists('temp'):
        os.mkdir('temp')
    for player in players:
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
    i=1
    for player in players:
        prevImage = os.path.join("temp/image", player, ".png")
        user = await client.fetch_user(players[i])
        await user.send(file=discord.File(prevImage))
        i=i+1
        if i>=len(players):
            i=0



@client.tree.command(description="Joins VC")
async def joinvc(interaction: discord.Interaction):
    channel = interaction.user.voice.voice_channel
    await client.join_voice_channel(channel)



client.run(TOKEN)
