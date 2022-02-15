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
        embed.add_field(
            name="Music Commands",
            value="join, leave, add, play, pause, \nskip, back, shuffle, loop, unloop, \nqueue, remove, clear, \nvolume (--help volume for more), \nlyrics, eq, aeq, nowplaying, skipto, \nrestart, seek ",
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
    
    # Music Help Commands
    @help.command()
    async def join(self, ctx):
        embed = help_embed(
            name="Join - Music Command.",
            description="Makes bot join voice channel that message author is in.",
            syntax="--[join|connect]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def leave(self, ctx):
        embed = help_embed(
            name="Leave - Music Command.",
            description="Makes bot leave voice channel.",
            syntax="--[leave|disconnect]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def add(self, ctx):
        embed = help_embed(
            name="Add - Music Command.",
            description="Shows top five results to choose from for request and adds to queue.",
            syntax="--[add|search] song-name"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def play(self, ctx):
        embed = help_embed(
            name="Play - Music Command.",
            description="Plays top result for request or continues playing songs",
            syntax="--play [song-name]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def pause(self, ctx):
        embed = help_embed(
            name="Pause - Music Command.",
            description="Pauses current track.",
            syntax="--[pause|stop]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def skip(self, ctx):
        embed = help_embed(
            name="Skip - Music Command.",
            description="Skips current track.",
            syntax="--[skip|next]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def back(self, ctx):
        embed = help_embed(
            name="Back - Music Command.",
            description="Plays previous song.",
            syntax="--[back|prev|previous]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def shuffle(self, ctx):
        embed = help_embed(
            name="Shuffle - Music Command.",
            description="Shuffles queue.",
            syntax="--[shuffle|mix]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def loop(self, ctx):
        embed = help_embed(
            name="Loop - Music Command.",
            description="Loops queue.",
            syntax="--loop"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def unloop(self, ctx):
        embed = help_embed(
            name="Un-Loop - Music Command.",
            description="Stops queue looping.",
            syntax="--unloop"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def queue(self, ctx):
        embed = help_embed(
            name="Queue - Music Command.",
            description="Shows song queue.",
            syntax="--queue num-elements"
        )
        await ctx.channel.send(embed=embed)
    
    @help.group()
    async def volume(self, ctx):
        embed = help_embed(
            name="Volume - Music Command.",
            description="Adjusts volume for bot, max is 150.",
            syntax="--[volume|vol] new-volume"
        )
        await ctx.channel.send(embed=embed)

    @volume.command()
    async def up(self, ctx):
        embed = help_embed(
            name="Up - Volume Command.",
            description="Increases volume by 10.",
            syntax="--[volume|vol] up"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def down(self, ctx):
        embed = help_embed(
            name="Down - Volume Command.",
            description="Lowers volume by 10.",
            syntax="--[volume|vol] down"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def reset(self, ctx):
        embed = help_embed(
            name="Reset - Volume Command.",
            description="Resets audio modifications.",
            syntax="--[volume|vol] reset"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def lyrics(self, ctx):
        embed = help_embed(
            name="Lyrics - Music Command.",
            description="Displays lyrics for current song or song of choice.",
            syntax="--lyrics [name]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def eq(self, ctx):
        embed = help_embed(
            name="Equalizer - Music Command.",
            description="Adjusts frequency bands to template: flat, boost, metal, piano.",
            syntax="--[eq|equalizer] [flat|boost|metal|piano]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def aeq(self, ctx):
        embed = help_embed(
            name="Advanced Equalizer - Music Command.",
            description="Change gain for given frequency band. Band: 1-15, Frequency: -10 - 10",
            syntax="--[aeq|adveq|advanced_equalizer] frequency-band gain"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def nowplaying(self, ctx):
        embed = help_embed(
            name="Now Playing - Music Command.",
            description="Shows information about current track.",
            syntax="--[nowplaying|np|playing]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def skipto(self, ctx):
        embed = help_embed(
            name="Skipto - Music Command.",
            description="Plays song at given index in queue.",
            syntax="--[skipto|playindex] index"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def restart(self, ctx):
        embed = help_embed(
            name="Restart - Music Command.",
            description="Restarts current track.",
            syntax="--[restart|again|replay]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def seek(self, ctx):
        embed = help_embed(
            name="Seek - Music Command.",
            description="Moves position in song to given index (mm:ss).",
            syntax="--[seek|to|move]"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def remove(self, ctx):
        embed = help_embed(
            name="Remove - Music Command.",
            description="Removes song at index from queue.",
            syntax="--remove index"
        )
        await ctx.channel.send(embed=embed)

    @help.command()
    async def clear(self, ctx):
        embed = help_embed(
            name="Clear - Music Command.",
            description="Clears queue.",
            syntax="--clear"
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

    
    
    
