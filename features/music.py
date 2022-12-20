import os
import discord
import time
from discord.ext import commands
from dotenv import load_dotenv
from pycord import wavelink
from tqdm import tqdm
# from wavelink.ext import spotify

load_dotenv()
# define guild ID
GUILD_THB = os.getenv('DISCORD_GUILD_BOTTEST')
GUILD_THB2 = os.getenv('DISCORD_GUILD_THB')


class CustomPlayer(wavelink.Player):

    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()


# noinspection PyTypeChecker
class Music(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

        bot.loop.create_task(self.connect_nodes())

    # helper function
    async def connect_nodes(self):
        time.sleep(1)
        print("---------------------------------------------------------------------------")
        for _ in tqdm(range(1), desc='Connectig nodes...', ascii=False, ncols=75, colour='CYAN'):
            time.sleep(1)
        print("Complete.")

        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host='192.168.10.210',
            port=2705,
            password='COMMD0m@!n',
            https=False
        )

    # noinspection PyGlobalUndefined
    @discord.slash_command(name="play", guild_ids=[GUILD_THB, GUILD_THB2])
    async def play(self, ctx, *, artist: str, name: str):
        """Play a song with the given search query.
        If not connected, connect to our voice channel.
        """
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        global search
        global partial
        global p_name
        global p_artist

        search = str(name + " " + artist)
        partial = wavelink.PartialTrack(query=search, cls=wavelink.YouTubeTrack)
        p_name = name
        p_artist = artist

        await vc.play(partial)
        await ctx.respond(f'**Now Playing:** ' + str.title(p_artist) + " - " + str.title(p_name))
        return partial

    @discord.slash_command(name="pause", guild_ids=[GUILD_THB, GUILD_THB2])
    async def pause(self, ctx):
        vc = ctx.voice_client
        if vc:
            if vc.is_playing() and not vc.is_paused():
                await vc.pause()
                await ctx.respond(f'**Paused:** ' + str.title(p_artist) + " - " + str.title(p_name))
            else:
                await ctx.send("Nothing is playing.")
        else:
            await ctx.send("The bot is not connected to a voice channel")

    @discord.slash_command(name="resume", guild_ids=[GUILD_THB, GUILD_THB2])
    async def resume(self, ctx):
        vc = ctx.voice_client
        if vc:
            if vc.is_paused():
                await vc.resume()
                await ctx.respond(f'**Now Playing:** ' + str.title(p_artist) + " - " + str.title(p_name))
            else:
                await ctx.send("Nothing is paused.")
        else:
            await ctx.send("The bot is not connected to a voice channel")

    # events
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print("---------------------------------------------------------------------------")
        print(f'Node: <{node.identifier}> is ready!')
        print("---------------------------------------------------------------------------")

    """
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('**Now Playing:**'):
            embed = discord.Embed(title='The Hangout Bot Music Player', description='Current song info', color=0xE91E63)
            embed.add_field(name=str.title(p_artist) + " - " + str.title(p_name),
                            value="is playing")
            embed_message = await message.channel.send(embed=embed)
            await embed_message.add_reaction("▶️")
            await embed_message.add_reaction("⏸️")
            await embed_message.add_reaction("⏯️")
            await embed_message.add_reaction("⏹️")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx, payload: discord.RawReactionActionEvent):
        time.sleep(1)

        # This section is for reaction roles#
        #####################################
        react_message_id = (
            1053779735412482188  # ID of the message that can be reacted to for adding/removing a role.
        )

        emoji_to_action = {
            discord.PartialEmoji(
                name="▶️"
            ): 10,  # Play button.
            discord.PartialEmoji(
                name="⏸️"
            ): 11,  # Pause button.
            discord.PartialEmoji(
                name="⏯️"
            ): 12,  # Skip button.
            discord.PartialEmoji(
                name="⏹️"
            ): 13  # Stop button.
        }

        if payload.message_id != react_message_id:
            return

        action = emoji_to_action[payload.emoji]

        if action == 10:
            await self.resume(self, ctx)
        elif action == 11:
            await self.pause(self, ctx)
        elif action == 12:
            await ctx.respond("Not built yet")
        elif action == 13:
            await ctx.respond("Not built yet")
        else:
            return
    """
    
    '''
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: CustomPlayer):
        if not player.queue.is_empty:
            next_track = player.queue.get()
            await player.play(next_track)

    # commands
    @discord.slash_command(guild_ids=[GUILD_THB, GUILD_THB2])
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Joins the bot to the voice channel"""  # The command description
        try:
            channel = channel or ctx.author.channel.voice
        except AttributeError:
            return await ctx.send('No voice channel to connect to. Please either provide one or join one.')

            # vc is short for voice client...
            # Our "vc" will be our wavelink.Player as type hinted below...
            # wavelink.Player is also a VoiceProtocol...

        vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
        return vc

    @discord.slash_command(guild_ids=[GUILD_THB, GUILD_THB2])
    async def disconnect(self, ctx):
        """Disconnects the bot from the voice channel"""
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
            return await ctx.send("The bot has disconnected from the voice channel.")
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    '''
    """
    @discord.slash_command(guild_ids=[GUILD_THB, GUILD_THB2])
    async def play(self, ctx, *, search: wavelink.YouTubeTrack):
        """'Plays song from search'"""
        vc = ctx.voice_client
        if not vc:
            await ctx.send("The bot is not connected to a voice channel.")

        if vc.is_playing():

            vc.queue.put(item=search)

            await ctx.send(embed=discord.Embed(
                title=search.title,
                url=search.uri,
                # author=ctx.author,
                description=f"Queued {search.title} in {vc.channel}"
            ))
        else:
            await vc.play(search)

            await ctx.send(embed=discord.Embed(
                title=vc.source.title,
                url=vc.source.uri,
                # author=ctx.author,
                description=f"Playing {vc.source.title} in {vc.channel}"
            ))

    @discord.slash_command(guild_ids=[GUILD_THB, GUILD_THB2])
    async def skip(self, ctx):
        """'Skips to the next song'"""
        vc = ctx.voice_client
        if vc:
            if not vc.is_playing():
                return await ctx.send("Nothing is playing.")
            if vc.queue.is_empty:
                await vc.stop()
                await ctx.send("The queue is empty.")

            await vc.seek(vc.track.length * 1000)
            if vc.is_paused():
                await vc.resume()
                return await ctx.send("Skipped to the next song.")
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @discord.slash_command(guild_ids=[GUILD_THB, GUILD_THB2])
    async def pause(self, ctx):
        """'Pauses the currently playing song'"""
        vc = ctx.voice_client
        if vc:
            if vc.is_playing() and not vc.is_paused():
                await vc.pause()
                return await ctx.send("The song is paused.")
            else:
                await ctx.send("Nothing is playing.")
        else:
            await ctx.send("The bot is not connected to a voice channel")

    @discord.slash_command(guild_ids=[GUILD_THB, GUILD_THB2])
    async def resume(self, ctx):
        """'Resumes the paused song'"""
        vc = ctx.voice_client
        if vc:
            if vc.is_paused():
                await vc.resume()
                return await ctx.send("Song has resumed.")
            else:
                await ctx.send("Nothing is paused.")
        else:
            await ctx.send("The bot is not connected to a voice channel")

    # error handling
    
    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send("Could not find a track.")
        else:
            return await ctx.send("Please join a voice channel.")
    """


def setup(bot):
    bot.add_cog(Music(bot))
    print("---------------------------------------------------------------------------")
    for _ in tqdm(range(1), desc='Loading Music extension...', ascii=False, ncols=75, colour='CYAN'):
        time.sleep(1)
    print("Complete.")
