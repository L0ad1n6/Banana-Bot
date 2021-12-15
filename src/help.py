import discord
from discord.ext import commands

def help_embed(name, description, syntax):
    embed = discord.Embed(
        title=name,
        color=0xfce303
    )
    embed.add_field(
        name="Desription",
        value=description,
        inline=False
    )
    embed.add_field(
        name="Syntax",
        value=syntax,
        inline=False
    )
    return embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def help(self):
        return
    
    # Moderation Help Commands
    @help.command()
    async def ban(self, ctx):
        embed = help_embed(
            name="Ban - Administrator Command",
            description="Bans members.",
            syntax="b![ban|evict] <user> [reason]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def kick(self, ctx):
        embed = help_embed(
            name="Kick - Administrator Command",
            description="Kicks members.",
            syntax="b![kick|yeet] <user> [reason]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def lock(self, ctx):
        embed = help_embed(
            name="Lock - Administrator Command",
            description="Locks channel, if no channel is specified current channel is locked.",
            syntax="b![lock|lockdown|panic] [channel]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def mute(self, ctx):
        embed = help_embed(
            name="Mute - Administrator Command",
            description="Mutes members.",
            syntax="b![mute|silence|censor] <user> [reason]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def setslow(self, ctx):
        embed = help_embed(
            name="Set Slowmode - Administrator Command",
            description="Sets slowmode of current channel.",
            syntax="b![setslow|slow|slowmode] <seconds>"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def unban(self, ctx):
        embed = help_embed(
            name="Unban - Administrator Command",
            description="Unbans user.",
            syntax="b![unban|pardon] <user>"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def unlock(self, ctx):
        embed = help_embed(
            name="Unlock - Administrator Command",
            description="Unlocks channel.",
            syntax="b![unlock|open|calm] [channel]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def unmute(self, ctx):
        embed = help_embed(
            name="Unmute - Administrator Command",
            description="Unmutes user.",
            syntax="b![unmute|unsilence|uncensor] <user>"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def warn(self, ctx):
        embed = help_embed(
            name="Warn - Administrator Command",
            description="Warns user for specified reason, used to keep track of punishements and mis behavior.",
            syntax="b!warn <user> [warning]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def warns(self, ctx):
        embed = help_embed(
            name="Unban - Administrator Command",
            description="Unbans user.",
            syntax="b![warns|warnings] [all|clear|warn index|none] [user]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def purge(self, ctx):
        embed = help_embed(
            name="Unban - Administrator Command",
            description="Unbans user.",
            syntax="b![warns|warnings] [all|clear|warn index|none] [user]"
        )
        await ctx.channel.send(embed=embed)
    
    # Social Credit Help Commands
    @help.command()
    async def cred(self, ctx):
        return
    
    @help.command()
    async def addcred(self, ctx):
        return
    
    @help.command()
    async def subcred(self, ctx):
        return
    
    @help.command()
    async def resetcred(self, ctx):
        return
    
    @help.command()
    async def setcred(self, ctx):
        return
    
    # Utility Help Commands
    @help.command()
    async def lastdeleted(self, ctx):
        return
    
    @help.command()
    async def whois(self, ctx):
        return
    
    @help.command()
    async def spam(self, ctx):
        return
    
    @help.command()
    async def invite(self, ctx):
        return
    
    
