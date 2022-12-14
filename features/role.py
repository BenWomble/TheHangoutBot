import os
import time
import discord
from tqdm import tqdm
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
# define guild ID
GUILD_THB = os.getenv('DISCORD_GUILD_BOTTEST')
GUILD_THB2 = os.getenv('DISCORD_GUILD_THB')
# define member join role
HELPERS_ROLE = os.getenv('HELPERS_ROLE')


class Role(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    # This section is for member joining#
    #####################################
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        if (
                guild.system_channel is not None
        ):  # For this to work, System Messages Channel should be set in guild settings.
            await guild.system_channel.send(f"Welcome {member.mention} to {guild.name}!")
            role = guild.get_role(int(HELPERS_ROLE))
            print(f"{member.name} (ID: {member.id}) has joined the server. Adding them to ({role}).")
            await member.add_roles(role)
            print(f"{member.name} (ID: {member.id}) has been added to the ({role}) role.")
            print("---------------------------------------------------------------------------")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """'Gives a role based on a reaction emoji.'"""
        # Make sure that the message the user is reacting to is the one we care about.
        time.sleep(1)

        # This section is for reaction roles#
        #####################################
        role_message_id = (
            1053779735412482188  # ID of the message that can be reacted to for adding/removing a role.
        )

        emoji_to_role = {
            discord.PartialEmoji(
                name="🟢"  # , id=1053792606305407046
            ): 1041387104992776230,  # ID of the role (Developers) associated with unicode emoji "🟢".
            discord.PartialEmoji(
                name="🟡"  # , id=1053792726136660079
            ): 1041387104992776229,  # ID of the role (Helpers) associated with unicode emoji "🟡".
            discord.PartialEmoji(
                name="🔴"  # , id=1053792766997569577
            ): 1053800205310496848,  # ID of the role (Bots) associated with unicode emoji "🔴".
        }

        if payload.message_id != role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        print("---------------------------------------------------------------------------")
        print("|                             Event Log:                                  |")
        print("---------------------------------------------------------------------------")
        print(f"Logging - adding {payload.member} member to role.")
        print(f"Guild: {guild}")
        role_id = emoji_to_role[payload.emoji]
        print(f"Role ID: {role_id}")
        role = guild.get_role(role_id)
        print(f"Role: {role}")
        print(f"Member: {payload.member}")
        await payload.member.add_roles(role)
        print("---------------------------------------------------------------------------")
        print(f"{payload.member} was added to {role}!")
        print("---------------------------------------------------------------------------")


def setup(bot):
    bot.add_cog(Role(bot))
    print("---------------------------------------------------------------------------")
    time.sleep(1)
    for _ in tqdm(range(1), desc='Loading Role extension...', ascii=False, ncols=75, colour='CYAN'):
        time.sleep(1)
    print("Complete.")
