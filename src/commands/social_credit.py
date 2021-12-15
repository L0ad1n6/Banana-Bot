import discord
from discord.ext import commands

class SocialCredit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def cred(self, ctx):
        return
    
    @commands.command()
    async def addcred(self, ctx):
        return
    
    @commands.command()
    async def subcred(self, ctx):
        return
    
    @commands.command()
    async def resetcred(self, ctx):
        return
    
    @commands.command()
    async def setcred(self, ctx):
        return

    @commands.Cog.listener()
    async def on_message(self, ctx):
        return
    
    