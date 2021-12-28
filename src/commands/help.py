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
    async def help(self, ctx):
        embed = discord.Embed(
            title="Command Index", 
            description="List of all available commands.",
            color=0xfce303
        )
        embed.add_field(
            name="Moderation",
            value="ban, kick, lock, mute, setslow,\nnunban, unlock, unmute, warn,\nwarns, purge",
            inline=False
        )
        embed.add_field(
            name="Social Credit",
            value="cred (\"--help cred\" for more credit commands)",
            inline=False
        )
        await ctx.channel.send(embed=embed)
    
    # Moderation Help Commands
    @help.command()
    async def ban(self, ctx):
        embed = help_embed(
            name="Ban - Administrator Command",
            description="Bans members.",
            syntax="--[ban|evict] <user> [reason]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def kick(self, ctx):
        embed = help_embed(
            name="Kick - Administrator Command",
            description="Kicks members.",
            syntax="--[kick|yeet] <user> [reason]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def lock(self, ctx):
        embed = help_embed(
            name="Lock - Administrator Command",
            description="Locks channel, if no channel is specified current channel is locked.",
            syntax="--[lock|lockdown|panic] [channel]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def mute(self, ctx):
        embed = help_embed(
            name="Mute - Administrator Command",
            description="Mutes members.",
            syntax="--[mute|silence|censor] <user> [reason]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def setslow(self, ctx):
        embed = help_embed(
            name="Set Slowmode - Administrator Command",
            description="Sets slowmode of current channel.",
            syntax="--[setslow|slow|slowmode] <seconds>"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def unban(self, ctx):
        embed = help_embed(
            name="Unban - Administrator Command",
            description="Unbans user.",
            syntax="--[unban|pardon] <user>"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def unlock(self, ctx):
        embed = help_embed(
            name="Unlock - Administrator Command",
            description="Unlocks channel.",
            syntax="--[unlock|open|calm] [channel]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def unmute(self, ctx):
        embed = help_embed(
            name="Unmute - Administrator Command",
            description="Unmutes user.",
            syntax="--[unmute|unsilence|uncensor] <user>"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def warn(self, ctx):
        embed = help_embed(
            name="Warn - Administrator Command",
            description="Warns user for specified reason, used to keep track of punishements and mis behavior.",
            syntax="--warn <user> [warning]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def warns(self, ctx):
        embed = help_embed(
            name="Unban - Administrator Command",
            description="Unbans user.",
            syntax="--[warns|warnings] [all|clear|warn index|none] [user]"
        )
        await ctx.channel.send(embed=embed)
    
    @help.command()
    async def purge(self, ctx):
        embed = help_embed(
            name="Unban - Administrator Command",
            description="Unbans user.",
            syntax="--[warns|warnings] [all|clear|warn index|none] [user]"
        )
        await ctx.channel.send(embed=embed)
    
    # Social Credit Help Commands
    @help.group()
    async def cred(self, ctx):
        embed = help_embed(
            name="Cred - Social Credit Command",
            description="Displays user's social credit.\nCommands: add, reset, set, sub",
            syntax="--[cred|credits|credit] [user]"
        )
        await ctx.channel.send(embed=embed)
    
    @cred.command()
    async def add(self, ctx):
        embed = help_embed(
            name="Add - Adminstrator Command",
            description="Increases user's social credit by amount.",
            syntax="--cred [add|increase] <amount> [user]"
        )
        await ctx.channel.send(embed=embed)
    
    @cred.command()
    async def sub(self, ctx):
        embed = help_embed(
            name="Sub - Administrator Command",
            description="Decreases user's social credit by amount.",
            syntax="--cred [sub|subtract|reduce|decrease] <amount> [user]"
        )
        await ctx.channel.send(embed=embed)
    
    @cred.command()
    async def reset(self, ctx):
        embed = help_embed(
            name="Reset - Administrator Command",
            description="Resets user's social credit",
            syntax="--cred [reset|zero|restart] [user]"
        )
        await ctx.channel.send(embed=embed)
    
    @cred.command()
    async def set(self, ctx):
        embed = help_embed(
            name="Set - Administrator Command",
            description="Sets user's social credit to amount.",
            syntax="--cred set <amount> [user]"
        )
        await ctx.channel.send(embed=embed)
    
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
    
    
