import discord
from discord.ext import commands

import sys
sys.path.append("..")

from db import *

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted = ["test"]

    @commands.command()
    async def lastdeleted(self, ctx, arg=None):
        if arg == "all":
            await ctx.channel.send(self.deleted[-6:-1])
        await ctx.channel.send(self.deleted[0])
    
    @commands.command()
    async def whois(self, ctx, user: discord.Member):
        embed = discord.Embed(
            title=f"{user.name}#{user.discriminator} (```{user.id}```) \n{f'AKA ```{user.display_name}```' if user.display_name != user.name else ''}\n{'*User*' if not user.bot else '*Bot*'}",
            color=0xfce303
        )
        embed.add_field(
            name="Discord Join Date", 
            value=user.created_at.strftime("%d %B %Y at %H:%M:%S PM UTC")
        )
        embed.add_field(
            name="Guild Join Date",
            value=user.joined_at.strftime("%d %B %Y at %H:%M:%S PM UTC")
        )
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def whereis(self, ctx):
        return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, user: discord.Member, times: int, *, content):
        for _ in range(times):
            await user.send(content)

    @commands.command()
    async def invite(self, ctx):
        await ctx.channel.send("https://discord.com/api/oauth2/authorize?client_id=900922626283810876&permissions=8&scope=bot")

    @commands.command()
    async def roll(self, ctx, user: discord.Member):
        link = "https://docs.google.com/forms/d/1uLYDZcCzqlbHl-4ITT7rpRVKxpKqjHz18_qoiR9NQdY/viewform?edit_requested=true"
        embed = discord.Embed(
            title="Social Credit Opportunity",
            description=f"Fill out survey for social-credit: {link}",
            color=0xfce303
        )
        await user.send(embed=embed)

    @commands.command()
    async def poll(self, ctx):
        return

    @commands.command()
    async def dataset(self, ctx, status, *, phrase):
        return

    # @commands.Cog.listener()
    # async def on_message_delete(self, ctx, user):
    #     # await ctx.channel.send(ctx)
    #     # print("triggered")
    #     self.deleted.insert((ctx.content, ctx.author.id), 0)
    #     return
