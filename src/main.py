# bot.py
import os
import shutil
import asyncio
import discord
import re
from dotenv import load_dotenv
from utils import *

start_msg  = f"Welcome to GarlicTone! Round 1 has started!\nCome up with a prompt to be given to another player!"
prompt_msg = f"Another player has drawn the image below; can you guess what their prompt was?"
image_msg  = f"Another player has come up with the prompt below; draw an image based on their prompt for someone else to guess!"

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
        round = 2
        iteration = 1
        await ask_for_initial_prompt(players)
        await send_blank(players)
        await asyncio.sleep(30)
        await download_initial_image_and_send(players)
        while True:
            round = round+1
            if round>len(players):
                break
            await ask_for_prompt(players, iteration)
            round = round+1
            if round>len(players):
                break
            await send_blank(players)
            await asyncio.sleep(30)
            await download_image_and_send(players, iteration)


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
async def download_initial_image_and_send(players):
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
                imageName = "temp/image_" + player + "_" + "0.png"
                await latestmessage.attachments[0].save(imageName) # saves the file
                print("wins")
        else:
            # Not found the user
            print("Fuck")
    i=1 
    for player in players:
        prevImage = "temp/image_" + player + "_" + "0.png"
        user = await client.fetch_user(players[i])
        await user.send(file=discord.File(prevImage))
        i=i+1
        if i>=len(players):
            i=0

@client.event
async def download_image_and_send(players, round):
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
                imageName = "temp/image_" + player + "_" + str(round) + ".png"
                await latestmessage.attachments[0].save(imageName) # saves the file
                print("wins")
        else:
            # Not found the user
            print("Fuck")
    i=1
    for player in players:
        prevImage = "temp/image_" + player + "_" + str(round) + ".png"
        user = await client.fetch_user(players[i])
        await user.send(file=discord.File(prevImage))
        i=i+1
        if i>=len(players):
            i=0

async def send_blank(players):
    for player in players:
        user = await client.fetch_user(player)
        await user.send(file=discord.File('blankdrawing.png'))

async def ask_for_initial_prompt(players):
    for player in players:
        user = await client.fetch_user(player)
        await user.send("Enter a Prompt:")
    await asyncio.sleep(30)
    for player in players:
        user = await client.fetch_user(player)
        messages = [message async for message in user.history(limit=1)]
        latestmessage = messages[0]
        promptPath = "temp/" + "prompt_" + player + "_0.txt"
        promptFile = open(promptPath, 'w')
        promptFile.write(str(latestmessage.content))
        promptFile.close()
    for i in range(len(players)):
        if i == len(players)-1:
            user = await client.fetch_user(players[0])
        else:
            user = await client.fetch_user(players[i+1])
        prevPromptPath = "temp/" + "prompt_" + players[i] + "_0.txt"
        prevPrompt = open(prevPromptPath, 'r')
        prompt = prevPrompt.read()
        await user.send("Your prompt is " + prompt)

async def ask_for_prompt(players, round):
    for player in players:
        user = await client.fetch_user(player)
        await user.send("What is this image:")
    await asyncio.sleep(30)
    for player in players:
        user = await client.fetch_user(player)
        messages = [message async for message in user.history(limit=1)]
        latestmessage = messages[0]
        promptPath = "temp/" + "prompt_" + player + "_" + str(round) + ".txt"
        promptFile = open(promptPath, 'w')
        promptFile.write(str(latestmessage.content))
        promptFile.close()
    for i in range(len(players)):
        if i == len(players)-1:
            user = await client.fetch_user(players[0])
        else:
            user = await client.fetch_user(players[i+1])
        prevPromptPath = "temp/" + "prompt_" + players[i] + "_" + str(round) + ".txt"
        prevPrompt = open(prevPromptPath, 'r')
        prompt = prevPrompt.read()
        await user.send("Your prompt is " + prompt)




async def send_final_images(GuildChannel: channel):
    for file in os.listdir("temp/"):
        if file.startswith("final"):
            with open(file, 'rb') as f:
                image = discord.File(f)
                await channel.send(file=picture)


client.run(TOKEN)
