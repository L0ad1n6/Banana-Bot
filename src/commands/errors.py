import discord
from discord.ext import commands
from discord.ext.commands.errors import *

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
            msg = "<:yellowx:938093739283451964> No more songs left in queue"

        else:
            msg = "<:yellowx:938093739283451964> Something went wrong, try again or use --report"

        await ctx.reply(msg, mention_author=False)
    
