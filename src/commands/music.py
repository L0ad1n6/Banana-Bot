import asyncio
import datetime as dt
import random
import re
import typing as t
from enum import Enum

import aiohttp
import discord
import wavelink
from discord.ext import commands
from .errors import *

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
LYRICS_URL = "https://some-random-api.ml/lyrics?title="
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 450, 630, 1000, 1600, 2500, 4000, 10000, 16000)
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}

class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self._loop = False

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current(self):
        if not self._queue:
            raise EmptyQueue

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def next(self):
        if not self._queue:
            raise EmptyQueue

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise EmptyQueue

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise EmptyQueue

        self.position += 1

        if self.position < 0:
            return
        elif self.position > len(self._queue) - 1:
            if self._loop:
                self.position = 0
            else:
                return

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise EmptyQueue

        next = self.next
        random.shuffle(next)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(next)

    def loop(self, mode):
        self._loop = bool(mode)

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.eq_levels = [0.] * 15

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnected

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise UserNotConnected

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            await ctx.send("song does not exist")
            return

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        else:
            self.queue.add(tracks[0])
            await ctx.send(f"<:yellowcheck:934551782867214387> **Added** {tracks[0].title}")

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()
        
    async def search_tracks(self, ctx, tracks):
        if not tracks:
            await ctx.send("song does not exist")
            return

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(f"<:yellowcheck:934551782867214387> **Added** {tracks[0].title}")
            print(tracks[0].identifier)
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                await ctx.send(f"<:yellowcheck:934551782867214387> **Added** {tracks.title}")

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {track.title} ({track.length//60000}:{str(track.length%60).zfill(2)})"
                    for i, track in enumerate(tracks[:5])
                )
            ),
            color=0xfce303,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS)[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except EmptyQueue:
            pass


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink Node Ready: {node.identifier}")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False
        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        node = {
            "host": "127.0.0.1",
            "port": 2333,
            "rest_uri": "http://127.0.0.1:2333",
            "password": "youshallnotpass",
            "identifier": "MAIN",
            "region": "europe",
        }

        await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(aliases=["connect"])
    async def join(self, ctx):
        player = self.get_player(ctx)
        channel = await player.connect(ctx)
        await ctx.reply(f"<:yellowcheck:934551782867214387> **Joining** {channel}", mention_author=False)

    @commands.command(aliases=["disconnect"])
    async def leave(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.reply(f"<:yellowcheck:934551782867214387> **Leaving** {ctx.author.voice.channel}", mention_author=False)

    @commands.command(aliases=["search"])
    async def add(self, ctx, *, query):
        player = self.get_player(ctx)

        if not player.is_connected:
            raise NotConnected

        query = query.strip("<>")
        if not re.match(URL_REGEX, query):
            query = f"ytsearch:{query}"

        await player.search_tracks(ctx, await self.wavelink.get_tracks(query))

    @commands.command()
    async def play(self, ctx, *, query=None):
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if player.queue.is_empty:
                raise EmptyQueue

            await player.set_pause(False)
            await ctx.reply(f"<:yellowcheck:934551782867214387> **Resuming** {player.queue.current.title}", mention_author=False)

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))
        
    @commands.command()
    async def pause(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise NotPlaying

        await player.set_pause(True)
        await ctx.reply(f"<:yellowcheck:934551782867214387> **Pausing** {player.queue.current.title}", mention_author=False)

    @commands.command(aliases=["next"])
    async def skip(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.next:
            raise EmptyQueue

        await player.stop()
        await ctx.reply(f"<:yellowcheck:934551782867214387> **Now Playing** {player.queue.next[0].title}", mention_author=False)

    @commands.command(aliases=["prev", "back"])
    async def previous(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoHistory

        player.queue.position -= 2
        await player.stop()
        await ctx.reply(f"<:yellowcheck:934551782867214387> **Now Playing** {player.queue.next[0].title}", mention_author=False)

    @commands.command()
    async def shuffle(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.reply("<:yellowcheck:934551782867214387> **Shuffling** Queue", mention_author=False)

    @commands.command()
    async def loop(self, ctx):
        player = self.get_player(ctx)
        player.queue.loop(True)
        await ctx.reply(f"<:yellowcheck:934551782867214387> **Looping** Queue", mention_author=False)

    @commands.command()
    async def unloop(self, ctx):
        player = self.get_player(ctx)
        player.queue.loop(False)
        await ctx.reply(f"<:yellowcheck:934551782867214387> **Un-Looping** Queue", mention_author=False)

    @commands.command()
    async def queue(self, ctx, show: int = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise EmptyQueue

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current.length, 60000)

        embed = discord.Embed(
            title="Currently Playing",
            description=f"[{player.queue.current.title}]({player.queue.current.uri}) {int(position[0]):02}:{round(position[1]/1000):02} / {int(length[0])}:{round(length[1]/1000):02}",
            color=0xfce303,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Queue")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        if next := player.queue.next:
            embed.add_field(
                name="Next up",
                value="\n".join(f"`{i+1}` [{track.title}]({track.uri}) {int(divmod(track.length, 60000)[0]):02}:{round(divmod(track.length, 60000)[1]/1000):02}" for i, track in enumerate(next[:show])),
                inline=False
            )

        msg = await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def volume(self, ctx, volume: int):
        player = self.get_player(ctx)

        if volume < 0:
            raise VolumeTooLow

        if volume > 150:
            raise VolumeTooHigh

        await player.set_volume(volume)
        await ctx.reply(f"<:yellowcheck:934551782867214387> Volume set to {volume:,}%", mention_author=False)

    @volume.command()
    async def up(self, ctx):
        player = self.get_player(ctx)
        await player.set_volume(value := min(player.volume + 10, 150))
        await ctx.reply(f"<:yellowcheck:934551782867214387> Volume set to {value:,}%", mention_author=False)

    @volume.command()
    async def down(self, ctx):
        player = self.get_player(ctx)
        await player.set_volume(value := max(0, player.volume - 10))
        await ctx.reply(f"<:yellowcheck:934551782867214387> Volume set to {value:,}%", mention_author=False)

    @volume.command()
    async def earrape(self, ctx):
        player = self.get_player(ctx)
        await player.set_volume(1500)
        await ctx.reply(f"Shield your ears", mention_author=False)

    @volume.command()
    async def reset(self, ctx):
        player = self.get_player(ctx)
        await player.set_volume(100)
        await ctx.reply("<:yellowcheck:934551782867214387> **Reset** Audio Level", mention_author=False)

    @commands.command()
    async def lyrics(self, ctx, name=None):
        player = self.get_player(ctx)
        name = name or player.queue.current.title

        async with ctx.typing():
            async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
                if not 200 <= r.status <= 299:
                    raise NoLyrics

                data = await r.json()

                if len(data["lyrics"]) > 2000:
                    msgs = len(data["lyrics"]) // 2000 + 1

                    for i in range(msgs):
                        embed = discord.Embed(
                            title=data["title"],
                            description=data["lyrics"][i:i+min(2000, len(data["lyrics"][i:]))],
                            color=0xfce303,
                            timestamp=dt.datetime.utcnow(),
                        )
                        embed.set_thumbnail(url=data["thumbnail"]["genius"])
                        embed.set_author(name=data["author"])
                        await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        title=data["title"],
                        description=data["lyrics"],
                        color=0xfce303,
                        timestamp=dt.datetime.utcnow(),
                    )
                    embed.set_thumbnail(url=data["thumbnail"]["genius"])
                    embed.set_author(name=data["author"])
                    await ctx.send(embed=embed)

    @commands.command(aliases=["equalizer"])
    async def eq(self, ctx, preset: str):
        player = self.get_player(ctx)

        eq = getattr(wavelink.eqs.Equalizer, preset, None)
        if not eq:
            raise InvalidEQPreset

        await player.set_eq(eq())
        await ctx.send(f"Equaliser adjusted to the {preset} preset.")

    @commands.command(aliases=["aeq", "advanced_equalizer"])
    async def adveq(self, ctx, band: int, gain: float):
        player = self.get_player(ctx)

        if not 1 <= band <= 15 and band not in HZ_BANDS:
            raise NonExistentEQBand

        if band > 15:
            band = HZ_BANDS.index(band) + 1

        if abs(gain) > 10:
            raise EQGainOutOfBounds

        player.eq_levels[band - 1] = gain / 10
        eq = wavelink.eqs.Equalizer(levels=[(i, gain) for i, gain in enumerate(player.eq_levels)])
        await player.set_eq(eq)
        await ctx.send("Equaliser adjusted.")

    @commands.command(aliases=["np", "playing"])
    async def nowplaying(self, ctx):
        player = self.get_player(ctx)

        if not player.is_playing:
            raise NotPlaying

        embed = discord.Embed(
            title="Playback Information",
            color=0xfce303,
            timestamp=dt.datetime.utcnow(),
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Track title", value=f"[{player.queue.current.title}]({player.queue.current.uri})", inline=True)

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current.length, 60000)
        progress = player.position / player.queue.current.length
        embed.add_field(
            name="Position",
            value=f"{int(position[0]):02}:{round(position[1]/1000):02}{'-'*int(40*progress)}o{'-'*(40-int(40*progress))}{int(length[0]):02}:{round(length[1]/1000):02}",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="skipto", aliases=["playindex"])
    async def skipto(self, ctx, index: int):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise EmptyQueue

        if not 0 <= index <= player.queue.length:
            raise NoMoreSongs

        player.queue.position += index - 1
        await player.stop()

        await ctx.reply(f"<:yellowcheck:934551782867214387> **Now Playing** {player.queue.next[0].title}", mention_author=False)

    @commands.command(aliases=["again", "replay"])
    async def restart(self, ctx):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise EmptyQueue

        await player.seek(0)
        await ctx.reply("<:yellowcheck:934551782867214387> **Replaying** Song", mention_author=False)

    @commands.command(aliases=["to", "move"])
    async def seek(self, ctx, position: str):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise EmptyQueue

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTime

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        await ctx.reply(f"<:yellowcheck:934551782867214387> **Resuming Playback** at {position}", mention_author=False)