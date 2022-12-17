import asyncio
import os
import youtube_dl
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# define guild ID
GUILD_THB = os.getenv('DISCORD_GUILD_BOTTEST')
GUILD_THB2 = os.getenv('DISCORD_GUILD_THEHANGOUT')
# define member join role
MEMBER_ROLE = os.getenv('MEMBER_ROLE')

intents = discord.Intents.all()
# noinspection PyUnresolvedReferences
intents.message_content = True
# noinspection PyUnresolvedReferences
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "65.184.84.144",  # Bind to ipv4 since ipv6 addresses cause issues at certain times
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.AudioSource, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # Takes the first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot_: commands.Bot):
        self.bot = bot_

    @commands.slash_command(guild_ids=[GUILD_THB])
    async def join(self, ctx: commands.Context, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.slash_command(guild_ids=[GUILD_THB])
    async def play(self, ctx: commands.Context, *, url: str):
        """Plays from an url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        await ctx.send(f"Now playing: {player.title}")

    @commands.slash_command(guild_ids=[GUILD_THB])
    async def stream(self, ctx: commands.Context, *, url: str):
        """Streams from an url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        await ctx.send(f"Now playing: {player.title}")

    @commands.slash_command(guild_ids=[GUILD_THB])
    async def volume(self, ctx: commands.Context, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.slash_command(guild_ids=[GUILD_THB])
    async def stop(self, ctx: commands.Context):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect(force=True)

    @play.before_invoke
    # @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


intents = discord.Intents.default()
# noinspection PyUnresolvedReferences
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("/"),
    description="Relatively simple music bot example",
    intents=intents,
)

bot.add_cog(Music(bot))


# This section is for member joining#
#####################################
@bot.event
async def on_ready():
    print("---------------------------------------------------------------")
    print(f"| Logged in as {bot.user} (ID: {bot.user.id}) |")
    print("---------------------------------------------------------------")


@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    if (
        guild.system_channel is not None
    ):  # For this to work, System Messages Channel should be set in guild settings.
        await guild.system_channel.send(f"Welcome {member.mention} to {guild.name}!")
        role = guild.get_role(int(MEMBER_ROLE))
        print(f"{member.name} (ID: {member.id}) has joined the server. Adding them to ({role}).")
        await member.add_roles(role)
        print(f"{member.name} (ID: {member.id}) has been added to the ({role}) role.")
        print("---------------------------------------------------------------")


# This section is for slash commands#
#####################################
@bot.slash_command(guild_ids=[GUILD_THB])
async def hello(ctx: discord.ApplicationContext):
    """Say hello to the bot"""  # The command description
    await ctx.respond(f"Hello, {ctx.author}!")


@bot.slash_command(guild_ids=[GUILD_THB])
async def ping(ctx: discord.ApplicationContext):
    """Play ping pong"""  # The command description
    await ctx.respond("pong")


@bot.slash_command(guild_ids=[GUILD_THB])
async def green_circle(ctx: discord.ApplicationContext):
    """Play ping pong"""  # The command description
    await ctx.respond("pong")


"""
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


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """'Gives a role based on a reaction emoji.'"""
    # Make sure that the message the user is reacting to is the one we care about.
    if payload.message_id != role_message_id:
        return

    guild = bot.get_guild(payload.guild_id)
    role_id = emoji_to_role[payload.emoji]
    print(role_id)
    role = guild.get_role(role_id)
    print(role)
    print(payload.member)
    await payload.member.add_roles(role)
    print(f"{payload.member.user} was added to {role}!")
"""


bot.run(TOKEN)
