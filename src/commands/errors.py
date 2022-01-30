import discord
from discord.ext import commands
from discord.ext.commands.errors import *

class InsufficientCredit(commands.CommandError):
    pass

class InsufficientRole(commands.CommandError):
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

def err_embed(error, author):
    embed = discord.Embed(
        title=f"Error Occured",
        description=error,
        color=0xff1919
    )
    embed.set_footer(
        text=f"Command By {author}",
        icon_url=author.avatar_url
    )
    return embed

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = err_embed(
                error=f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds.",
                author=ctx.author
            )

        elif isinstance(error, MissingPermissions):
            embed = err_embed(
                error=f"{ctx.author} you are missing the required permissions to run this command!",
                author=ctx.author
            )

        elif isinstance(error, MissingRequiredArgument):
            embed = err_embed(
                error=f"Missing a required argument: **{error.param}**",
                author=ctx.author
            )

        elif isinstance(error, ConversionError):
            embed = err_embed(
                error=str(error),
                author=ctx.author
            )

        else:
            dev = self.bot.get_user(586902188899696653)
            report = discord.Embed(
                title="Un-Documented Event Has Occured",
            ) 
            dev.send()
            embed = err_embed(
                error=f"Uh oh. Something undocumented has occured please contact <@!586902188899696653> to fix it.",
                author=ctx.author
            )

        await ctx.channel.send(embed=embed)
