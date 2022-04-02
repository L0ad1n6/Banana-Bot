import discord
from discord.ext import commands
from .moderation import err_embed
from .errors import *

class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[Bot] Connection to discord established")
        activity = discord.Game(name="--help | Senatus Populusque Bananus", type=4)
        await self.bot.change_presence(status=discord.Status.idle, activity=activity)
