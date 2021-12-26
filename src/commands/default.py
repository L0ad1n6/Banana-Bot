import discord
from discord.ext import commands
from .moderation import err_embed

class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to discord.")
        activity = discord.Game(name="--help | Senatus Populusque Bananus", type=4)
        await self.bot.change_presence(status=discord.Status.idle, activity=activity)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            embed = err_embed(
                error=f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds.",
                author=ctx.author
            )

        elif isinstance(error, commands.errors.MissingPermissions):
            embed = err_embed(
                error=f"{ctx.author} you are missing the required permissions to run this command!",
                author=ctx.author
            )

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            embed = err_embed(
                error=f"Missing a required argument: **{error.param}**",
                author=ctx.author
            )

        elif isinstance(error, commands.errors.ConversionError):
            embed = err_embed(
                error=str(error),
                author=ctx.author
            )
        else:
            embed = err_embed(
                error=f"Oh no! Something went wrong while running the command!",
                author=ctx.author
            )

        await ctx.channel.send(embed=embed)
