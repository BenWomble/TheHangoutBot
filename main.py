import os
import sys
import traceback
import discord
import time
from tqdm import tqdm
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
# noinspection PyUnresolvedReferences
intents.message_content = True
# noinspection PyUnresolvedReferences
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

startup_extensions = ['role', 'slash']


@bot.event
async def on_ready():
    print("---------------------------------------------------------------------------")
    time.sleep(1)
    for _ in tqdm(range(1), desc='Loading Bot...', ascii=False, ncols=75, colour='CYAN'):
        time.sleep(1)
    print("Complete.")
    print("---------------------------------------------------------------------------")
    print("")
    print("")
    time.sleep(3)
    print("---------------------------------------------------------------------------")
    print(f"|       Logged in as {bot.user} (ID: {bot.user.id})       |")
    print("---------------------------------------------------------------------------")


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            time.sleep(3)
        except (Exception,):
            print('Failed to load extension ' + extension + '.', file=sys.stderr)
            traceback.print_exc()
    bot.run(TOKEN)
