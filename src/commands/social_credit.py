import discord
from discord.ext import commands
from discord.utils import get
import lightgbm as lgb
import numpy as np
from .moderation import com_embed

import sys
sys.path.append("../")

from db import *

def b10(string):
    string = list(filter(str.isalnum, string.lower()))
    return int("1"+("".join([str(ord(char)).zfill(3) for char in string])))

class SocialCredit(commands.Cog):
    def __init__(self, bot):
        self.model = lgb.Booster(model_file="src/data/model/model.txt")
        self.bot = bot
    
    @commands.group(invoke_without_command=True, aliases=["credits", "credit"])
    async def cred(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        data = get_user(user.id)

        if not data:
            create_user(user.id)
            data = get_user(user.id)

        embed = com_embed(
            title=f"****{user}'s**** Social Credit",
            description=f"Social Credit: {data['social_credit']}",
            footer=f"Command By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)

    @cred.command(aliases=["increase"])
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, amount: int, user: discord.Member=None):
        user = user or ctx.author
        data = get_user(user.id)

        if not data:
            create_user(user.id)

        add_credits(user.id, amount)
        data = get_user(user.id)

        embed = com_embed(
            title=f"****{user}'s**** Social Credit has been ****INCREASED****",
            description=f"New Social Credit: {data['social_credit']}",
            footer=f"Added By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
        await user.send(f"```Your Social Credit on The Peoples Republic of Banana has been updated```")
        await user.send(embed=embed)
    
    @cred.command(aliases=["subtract", "reduce", "decrease"])
    @commands.has_permissions(administrator=True)
    async def sub(self, ctx, amount: int, user: discord.Member=None):
        user = user or ctx.author
        data = get_user(user.id)

        if not data:
            create_user(user.id)

        sub_credits(user.id, amount)
        data = get_user(user.id)

        embed = com_embed(
            title=f"****{user}'s**** Social Credit has been ****REDUCED****",
            description=f"New Social Credit: {data['social_credit']}",
            footer=f"Subtracted By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
        await user.send(f"```Your Social Credit on The Peoples Republic of Banana has been updated```")
        await user.send(embed=embed)
    
    @cred.command(aliases=["zero", "restart"])
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        data = get_user(user.id)

        if not data:
            create_user(user.id)

        reset_credits(user.id)

        embed = com_embed(
            title=f"****{user}'s**** Social Credit has been ****RESET****",
            description=f"New Social Credit: 0",
            footer=f"Reset By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
        await user.send(f"```Your Social Credit on The Peoples Republic of Banana has been updated```")
        await user.send(embed=embed)
    
    @cred.command()
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, amount: int, user: discord.Member=None):
        user = user or ctx.author
        data = get_user(user.id)

        if not data:
            create_user(user.id)

        set_credits(user.id, amount)

        embed = com_embed(
            title=f"****{user}'s**** Social Credit has been ****SET****",
            description=f"New Social Credit: {amount}",
            footer=f"Set By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
        await user.send(f"```Your Social Credit on The Peoples Republic of Banana has been updated```")
        await user.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return

        msg = ctx.content
        formatted = np.array(b10(msg)).reshape((1, 1))
        prediction = list(self.model.predict(formatted)[0])
        i = prediction.index(max(prediction))

        if i != 1:
            data = get_user(ctx.author.id)

            if not data:
                create_user(ctx.author.id)
                data = get_user(ctx.author.id)

            if i == 0:
                sub_credits(ctx.author.id, 15*prediction[i]+(len(data["warns"])+1)*3)
                add_point(msg, "bad")

            elif i == 1:
                add_point(msg, "neutral")

            elif i == 2:
                add_credits(ctx.author.id, 15*prediction[i])
                add_point(msg, "good")
