from discord.ext import commands
from discord.ext.commands.errors import *
from .music import HZ_BANDS
from wavelink.errors import ZeroConnectedNodes
import os
import sys

class InsufficientCredit(commands.CommandError):
    pass
class InsufficientRole(commands.CommandError):
    pass
class UserNotConnected(commands.CommandError):
    pass
class NotConnected(commands.CommandError):
    pass
class AlreadyConnected(commands.CommandError):
    pass
class NotPlaying(commands.CommandError):
    pass
class AlreadyPlaying(commands.CommandError):
    pass
class EmptyQueue(commands.CommandError):
    pass
class NoMoreSongs(commands.CommandError):
    pass
class NoHistory(commands.CommandError):
    pass
class InvalidTime(commands.CommandError):
    pass
class VolumeTooLow(commands.CommandError):
    pass
class VolumeTooHigh(commands.CommandError):
    pass
class NoLyrics(commands.CommandError):
    pass
class InvalidEQPreset(commands.CommandError):
    pass
class NonExistentEQBand(commands.CommandError):
    pass
class EQGainOutOfBounds(commands.CommandError):
    pass

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, CommandOnCooldown):
            msg = f"<:yellowx:938093739283451964> Command is on **cooldown**, try again in {round(error.retry_after, 1)} seconds"

        elif isinstance(error, MissingPermissions):
            msg = "<:yellowx:938093739283451964> Cannot run command, missing permissions"

        elif isinstance(error, MissingRequiredArgument):
            msg = f"<:yellowx:938093739283451964> Missing required argument: **{error.param}**"

        elif isinstance(error, ConversionError):
            msg = "<:yellowx:938093739283451964> Invalid argument type, could not convert"

        elif isinstance(error, CommandNotFound):
            msg = "<:yellowx:938093739283451964> The command you are trying to use does not exist"

        elif isinstance(error, InsufficientCredit):
            msg = "<:yellowx:938093739283451964> You do not have enough Social Credit to perform this action"

        elif isinstance(error, InsufficientRole):
            msg = "<:yellowx:938093739283451964> Your top role is not high enough to perform this action"

        elif isinstance(error, UserNotConnected):
            msg = "<:yellowx:938093739283451964> You are not connected to a voice channel"

        elif isinstance(error, NotConnected):
            msg = "<:yellowx:938093739283451964> I'm not connected to a voice channel"

        elif isinstance(error, AlreadyConnected):
            msg = "<:yellowx:938093739283451964> I'm already connected to a voice channel"

        elif isinstance(error, NotPlaying):
            msg = "<:yellowx:938093739283451964> Music is not playing"

        elif isinstance(error, AlreadyPlaying):
            msg = "<:yellowx:938093739283451964> Music is already playing"

        elif isinstance(error, EmptyQueue):
            msg = "<:yellowx:938093739283451964> Queue is empty"

        elif isinstance(error, NoMoreSongs):
            msg = "<:yellowx:938093739283451964> No more songs left in queue"

        elif isinstance(error, NoHistory):
            msg = "<:yellowx:938093739283451964> No songs have been played yet"

        elif isinstance(error, InvalidTime):
            msg = "<:yellowx:938093739283451964> Time formatting is invalid"

        elif isinstance(error, VolumeTooHigh):
            msg = "<:yellowx:938093739283451964> You will kill your ears if I set the volume any higher than 150% (capable of 1500%)"

        elif isinstance(error, VolumeTooLow):
            msg = "<:yellowx:938093739283451964> Volume must be greater than 0"

        elif isinstance(error, NoLyrics):
            msg = "<:yellowx:938093739283451964> No lyrics found for this song"

        elif isinstance(error, InvalidEQPreset):
            msg = "<:yellowx:938093739283451964> EQ preset must be one of the following: flat, boost, metal, piano"

        elif isinstance(error, NonExistentEQBand):
            msg = f"<:yellowx:938093739283451964> This is a 15 band equalizer, the band number should be between 1 and 15 or one of of the frequencies: {', '.join(str(band) for band in HZ_BANDS)}"

        elif isinstance(error, EQGainOutOfBounds):
            msg = "<:yellowx:938093739283451964> EQ Gain for any band should be between -10 db and 10 db. Though possible anything more will kill your ears"

        elif isinstance(error, ZeroConnectedNodes):
            msg = "<:yellowx:938093739283451964> Lavalink server is offline, bot will reboot to fix this."
            print("Restarting...")
            os.execl(sys.executable, os.path.abspath("src/main.py")) 

        else:
            msg = "<:yellowx:938093739283451964> Something went wrong, try again or use --report"
            await ctx.reply(msg, mention_author=False)
            raise error

        await ctx.reply(msg, mention_author=False)
    
