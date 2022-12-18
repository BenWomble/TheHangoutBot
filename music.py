# import asyncio
# import os
import discord
import main
import time
from discord.ext import commands
# from dotenv import load_dotenv
from pycord import wavelink
from tqdm import tqdm
# from wavelink.ext import spotify


class CustomPlayer(wavelink.Player):

    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()


class Music(discord.Cog):
    print("Music extension is loading......")

    def __init__(self, bot):
        self.bot = bot

    # helper function
    async def connect_nodes(self):
        await main.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=main.bot,
            host='jp-lava.islantay.tk',
            port=443,
            password='AmeliaWatsonisTheBest**!',
            https=True
        )

    # events
    @main.bot.event
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node: <{node.identifier}> is ready!')

    @main.bot.event
    async def on_wavelink_track_end(self, player: CustomPlayer, track: wavelink.Track, reason):
        if not player.queue.is_empty:
            next_track = player.queue.get()
            await player.play(next_track)

    # commands
    @main.bot.slash_command(guild_ids=[main.GUILD_THB])
    async def join(self, ctx, channel: discord.VoiceChannel = None):
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

    @main.bot.slash_command(guild_ids=[main.GUILD_THB])
    async def disconnect(self, ctx):
        """Disconnects the bot from the voice channel"""
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
            return await ctx.send("The bot has disconnected from the voice channel.")
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @main.bot.slash_command(guild_ids=[main.GUILD_THB])
    async def play(self, ctx, *, search: wavelink.YouTubeTrack):
        """Plays song from search"""
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

    @main.bot.slash_command(guild_ids=[main.GUILD_THB])
    async def skip(self, ctx):
        """Skips to the next song"""
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

    @main.bot.slash_command(guild_ids=[main.GUILD_THB])
    async def pause(self, ctx):
        """Pauses the currently playing song"""
        vc = ctx.voice_client
        if vc:
            if vc.is_playing() and not vc.is_paused():
                await vc.pause()
                return await ctx.send("The song is paused.")
            else:
                await ctx.send("Nothing is playing.")
        else:
            await ctx.send("The bot is not connected to a voice channel")

    @main.bot.slash_command(guild_ids=[main.GUILD_THB])
    async def resume(self, ctx):
        """Resumes the paused song"""
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


def setup(bot):
    bot.add_cog(Music(bot))
    print("")
    print("---------------------------------------------------------------------------")
    for _ in tqdm(range(10), desc='Loading Music extension...', ascii=False, ncols=75, colour='CYAN'):
        time.sleep(1)
    print("Complete.")
