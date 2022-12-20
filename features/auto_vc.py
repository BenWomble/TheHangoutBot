import discord
import time
from tqdm import tqdm
from discord.ext import commands


class AutoVC(discord.Cog):

    temporary_channels = []
    temporary_categories = []

    def __init__(self, bot):
        self.bot = bot

    # This section is for voice channel joining#
    ############################################
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        possible_channel_name = f"{member.name}'s channel"
        if after.channel.name == 'join to create own channel':
            temp_channel = await after.channel.clone(name=possible_channel_name)
            await member.move_to(temp_channel)
            self.temporary_channels.append(temp_channel.id)

        if before.channel:
            if before.channel.id in self.temporary_channels:
                if len(before.channel.members) == 0:
                    await before.channel.delete()


def setup(bot):
    bot.add_cog(AutoVC(bot))
    print("---------------------------------------------------------------------------")
    time.sleep(1)
    for _ in tqdm(range(1), desc='Loading Auto VC extension...', ascii=False, ncols=75, colour='CYAN'):
        time.sleep(1)
    print("Complete.")
