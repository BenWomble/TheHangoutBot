import os
import discord
import time
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
# define guild ID
GUILD_THB = os.getenv('DISCORD_GUILD_BOTTEST')
GUILD_THB2 = os.getenv('DISCORD_GUILD_THB')


class Slash(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    # This section is for slash commands#
    #####################################
    @discord.slash_command(guild_ids=[GUILD_THB, GUILD_THB2])
    async def hello(self, ctx: discord.ApplicationContext):
        """Say hello to the bot"""  # The command description
        await ctx.respond(f"Hello, {ctx.author}!")

    @discord.slash_command(guild_ids=[GUILD_THB, GUILD_THB2])
    async def ping(self, ctx: discord.ApplicationContext):
        """Play ping pong"""  # The command description
        await ctx.respond("pong")


def setup(bot):
    bot.add_cog(Slash(bot))
    print("---------------------------------------------------------------------------")
    time.sleep(1)
    for _ in tqdm(range(1), desc='Loading Slash extension...', ascii=False, ncols=75, colour='CYAN'):
        time.sleep(1)
    print("Complete.")
