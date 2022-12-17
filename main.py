
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_BOTTEST = os.getenv('DISCORD_GUILD_BOTTEST')

intents = discord.Intents.default()

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.slash_command(guild_ids=[GUILD_BOTTEST])
async def hello(ctx: discord.ApplicationContext):
    """Say hello to the bot"""  # The command description can be supplied as the docstring
    await ctx.respond(f"Hello, {ctx.author}!")


bot.run(TOKEN)
