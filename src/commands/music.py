import discord
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
import asyncio, random
from .errors import *

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


def song_embed(title, song):
    embed = discord.Embed(
        title=title, 
        description=f"[{song['name']}]({song['url']})",
        color=0xfce303
    )
    embed.set_thumbnail(url=song["thumbnail"])
    embed.set_footer(text=f"Added by {song['author']}", icon_url=song["author"].avatar_url)
    return embed

def is_connected(ctx: commands.Context):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def is_playing(ctx: commands.Context):
    voice_client = ctx.guild.voice_client
    return voice_client and \
        voice_client.channel and \
        voice_client.source and \
        ctx.voice_client.is_playing()

def user_connected(ctx: commands.Context):
    try:
        return ctx.author.voice.channel
    except:
        return False

class Queue:
    def __init__(self):
        self.queue = []
        self.loop = False
    
    @property
    def now_playing(self):
        try:
            return self.queue[0]
        except IndexError:
            return None

    @property
    def last(self):
        try:
            return self.queue[-1]
        except IndexError:
            return None

    def next(self):
        song = self.queue.pop(0)
        if self.loop:
            self.queue.append(song)
        return self.now_playing

    def clear(self):
        self.queue = [self.queue[0]]

    def add(self, url, author):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)#['entries'][0]
        
        URL = info['entries'][0]['formats'][0]['url']
        source = discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
        song = {
            "name": info['entries'][0]["title"],
            "thumbnail": info['entries'][0]["thumbnail"] if "thumbnail" in info['entries'][0] else None,
            "url": info['entries'][0]["webpage_url"],
            "time": info['entries'][0]["duration"],
            "source": source,
            "author": author
        }
        self.queue.append(song)

    def remove(self, index):
        return self.queue.pop(index)

    def shuffle(self):
        temp = self.queue[1:]
        random.shuffle(temp)
        self.queue = [self.queue[0]] + temp

class AudioSourceTracked(discord.AudioSource):
    def __init__(self, source):
        self._source = source
        self.count_20ms = 0

    def read(self) -> bytes:
        data = self._source.read()
        if data:
            self.count_20ms += 1
        return data
        
    @property
    def progress(self) -> float:
        return self.count_20ms * 0.02 # count_20ms * 20ms
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.q = Queue()


    def _play(self, ctx, song, voice_client):
        def on_end(err):
            if len(self.q.queue) > 0:
                song = self.q.next()
                embed = song_embed("Now Playing", song)
                self._play(ctx, song["source"], voice_client)

            else:
                asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.bot.loop)
                raise EmptyQueue

            asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.bot.loop)
        
        voice_client.play(song, after=on_end)

    @commands.command()
    async def play(self, ctx: commands.Context, *, url=None):
        if not user_connected(ctx):
            raise UserNotConnected

        if not is_connected(ctx):
            await ctx.author.voice.channel.connect()

        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)

        playing = False
        if is_playing(ctx):
            playing = True

        if not url and not playing:
            song = self.q.now_playing
            embed = song_embed("Resuming Song", song)
            voice_client.resume()

        elif not url:
            raise AlreadyPlaying
        
        else:
            self.q.add(url, ctx.author)

            if not playing:
                song = self.q.now_playing
                embed = song_embed("Playing Song", song)
                self._play(ctx, song["source"], voice_client)

            else:
                song = self.q.last
                embed = song_embed("Added Song", song)
            
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx: commands.Context):
        if not user_connected(ctx):
            raise UserNotConnected

        if not is_connected(ctx):
            raise NotConnected

        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)

        if is_playing(ctx):
            voice_client.pause()

        song = self.q.next()

        if song:
            embed = song_embed("Now Playing", song, song["author"])
            self._play(ctx, song["source"], voice_client)
            await ctx.send(embed=embed)
        else:
            raise EmptyQueue
        
    @commands.command()
    async def queue(self, ctx):
        queue = ""
        for i, song in enumerate(self.q.queue):
            if i == 0:
                queue += f"[{song['name']}]({song['url']})\n"
            else:
                queue += f"\n`{i}` [{song['name']}]({song['url']}) "
                if song["time"] > 3600:
                    queue += f"{str(song['time']//3600).zfill(2)}:"
                queue += f"{str((song['time']%3600)//60).zfill(2)}:{str((song['time']%3600)%60).zfill(2)}"
        embed = discord.Embed(
            title=f"Queue ({len(self.q.queue)-1})",
            color=0xfce303
        )
        embed.add_field(
            name="Now Playing",
            value=queue if queue != f"[{song['name']}]({song['url']})\n" else queue + "\n**Add songs to queue with --play or --add**"
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx):
        if not user_connected(ctx):
            raise UserNotConnected

        if not is_connected(ctx):
            raise NotConnected

        self.q.clear()
        await ctx.channel.send("<:yellowcheck:934551782867214387> **Cleared** Queue")

    @commands.command()
    async def add(self, ctx, *, url):
        if not user_connected(ctx):
            raise UserNotConnected

        if not is_connected(ctx):
            raise NotConnected

        self.q.add(url)

    @commands.command()
    async def remove(self, ctx, i: int):
        if not user_connected(ctx):
            raise UserNotConnected

        if not is_connected(ctx):
            raise NotConnected

        song = self.q.remove(i)
        await ctx.channel.send(f"<:yellowcheck:934551782867214387> **Removed** {song['name']}")

    @commands.command()
    async def lyrics(self, ctx):
        song = self.q.now_playing

    @commands.command()
    async def loop(self, ctx):
        if not user_connected(ctx):
            raise UserNotConnected

        if not is_connected(ctx):
            raise NotConnected

        self.q.loop = True
        await ctx.channel.send("<:yellowcheck:934551782867214387> **Looping** Queue")

    @commands.command()
    async def unloop(self, ctx):
        if not user_connected(ctx):
            raise UserNotConnected

        if not is_connected(ctx):
            raise NotConnected

        self.q.loop = False
        await ctx.channel.send("<:yellowcheck:934551782867214387> **Unlooping** Queue")

    @commands.command()
    async def pause(self, ctx):
        if not user_connected(ctx):
            raise UserNotConnected

        if not is_connected(ctx):
            raise NotConnected

        if not is_playing(ctx):
            raise NotPlaying

        voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        voice_client.pause()
        await ctx.send(f"<:yellowcheck:934551782867214387> **Paused** {self.q.now_playing['name']}")
            
    @commands.command()
    async def join(self, ctx: commands.Context):
        if not user_connected(ctx):
            raise UserNotConnected

        if is_connected(ctx):
            raise AlreadyConnected

        vc = ctx.author.voice.channel
        await vc.connect()
        await ctx.reply(f"<:yellowcheck:934551782867214387> **Joining** {vc}", mention_author=False)

    @commands.command()
    async def leave(self, ctx):
        if not is_connected(ctx):
            raise NotConnected

        await ctx.voice_client.disconnect()
        await ctx.channel.send(f"<:yellowcheck:934551782867214387> **Leaving** {ctx.channel}")

    @commands.command()
    async def shuffle(self, ctx):
        if not user_connected(ctx):
            raise UserNotConnected

        if not is_connected(ctx):
            raise NotConnected

        self.q.shuffle()
        await ctx.send("<:yellowcheck:934551782867214387> **Shuffled** Queue")

    @commands.command()
    async def fastforward(self, ctx, seconds: int):
        return

    @commands.command()
    async def equalizer(self, ctx):
        return

    @commands.command()
    async def volume(self, ctx):
        return