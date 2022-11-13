import os
import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/hello'):
        await message.channel.send('Hello, world!')


client.run('MTA0MTM4NzI0NTkxMjk4OTgwNg.GHjC1r.oLkIlqIAk82yU8AxrD_LEjR8TE1u731iUdSC0I')
