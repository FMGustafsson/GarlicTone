import os
import shutil
import asyncio
import discord
import re
from dotenv import load_dotenv
async def cleanup_temp():
    shutil.rmtree(os.path.basename("temp/"))

async def join_vc(interaction: discord.Interaction):
    channel = interaction.user.voice.channel
    vc = await channel.connect()

# async def play_vc(audio_file: str, vc: VoiceClient):
#     vc.play(discord.FFmpegPCMAudio(audio_file))
#     return 1