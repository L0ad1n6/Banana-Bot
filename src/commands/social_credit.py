import discord
from discord.ext import commands
import lightgbm as lgb
import json
import numpy as np
from .moderation import com_embed
def b10(string):
    string = list(filter(str.isalnum, string.lower()))
    return int("1"+("".join([str(ord(char)).zfill(3) for char in string])))

class SocialCredit(commands.Cog):
    def __init__(self, bot):
        self.model = lgb.Booster(model_file="src/data/model.txt")
        self.bot = bot
    
    @commands.group(invoke_without_command=True, aliases=["credits", "credit"])
    async def cred(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        with open("src/data/users.json", "r") as f:
            users = json.load(f)

        if str(user.id) not in users:
            users.update({str(user.id):{"social_credit":0,"warns":[]}})

        embed = com_embed(
            title=f"****{user}'s**** Social Credit",
            description=f"Social Credit: {users[str(user.id)]['social_credit']}",
            footer=f"Command By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)

    @cred.command(aliases=["increase"])
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, amount: int, user: discord.Member=None):
        user = user or ctx.author
        with open("src/data/users.json", "r") as f:
            users = json.load(f)
            if str(user.id) not in users:
                users.update({str(user.id):{"social_credit":0,"warns":[]}})
            users[str(user.id)]["social_credit"] += amount

        with open("src/data/users.json", "w") as f:
            json.dump(users, f, indent=2)

        embed = com_embed(
            title=f"****{user}'s**** Social Credit has been ****INCREASED****",
            description=f"New Social Credit: {users[str(user.id)]['social_credit']}",
            footer=f"Added By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
        await user.send(f"```Your Social Credit on The Peoples Republic of Banana has been updated```")
        await user.send(embed=embed)
    
    @cred.command(aliases=["subtract", "reduce", "decrease"])
    @commands.has_permissions(administrator=True)
    async def sub(self, ctx, amount: int, user: discord.Member=None):
        user = user or ctx.author
        with open("src/data/users.json", "r") as f:
            users = json.load(f)
            if str(user.id) not in users:
                users.update({str(user.id):{"social_credit":0,"warns":[]}})
            users[str(user.id)]["social_credit"] -= amount

        with open("src/data/users.json", "w") as f:
            json.dump(users, f, indent=2)

        embed = com_embed(
            title=f"****{user}'s**** Social Credit has been ****REDUCED****",
            description=f"New Social Credit: {users[str(user.id)]['social_credit']}",
            footer=f"Subtracted By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
        await user.send(f"```Your Social Credit on The Peoples Republic of Banana has been updated```")
        await user.send(embed=embed)
    
    @cred.command(aliases=["zero", "restart"])
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        with open("src/data/users.json", "r") as f:
            users = json.load(f)
            if str(user.id) not in users:
                users.update({str(user.id):{"social_credit":0,"warns":[]}})
            users[str(user.id)]["social_credit"] = 0

        with open("src/data/users.json", "w") as f:
            json.dump(users, f, indent=2)

        embed = com_embed(
            title=f"****{user}'s**** Social Credit has been ****RESET****",
            description=f"New Social Credit: {users[str(user.id)]['social_credit']}",
            footer=f"Reset By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
        await user.send(f"```Your Social Credit on The Peoples Republic of Banana has been updated```")
        await user.send(embed=embed)
    
    @cred.command()
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, amount: int, user: discord.Member=None):
        user = user or ctx.author
        with open("src/data/users.json", "r") as f:
            users = json.load(f)
            if str(user.id) not in users:
                users.update({str(user.id):{"social_credit":0,"warns":[]}})
            users[str(user.id)]["social_credit"] = amount

        with open("src/data/users.json", "w") as f:
            json.dump(users, f, indent=2)

        embed = com_embed(
            title=f"****{user}'s**** Social Credit has been ****SET****",
            description=f"New Social Credit: {users[str(user.id)]['social_credit']}",
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
            with open("src/data/users.json", "r") as f:
                users = json.load(f)

            if str(ctx.author.id) not in users:
                users.update({str(ctx.author.id):{"social_credit":0,"warns":[]}})

            if i == 0:
                users[str(ctx.author.id)]["social_credit"] -= 15*prediction[i]+(len(users[str(ctx.author.id)]["warns"])+1)*3

            elif i == 2:
                users[str(ctx.author.id)]["social_credit"] += 15*prediction[i]

            with open("src/data/users.json", "w") as f:
                json.dump(users, f, indent=2)
