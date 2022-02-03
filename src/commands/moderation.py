import discord
from discord.ext import commands
import time
from .errors import *

import sys
sys.path.append("..")

from db import *

def com_embed(title, description, footer):
    embed = discord.Embed(
        title=title,
        description=description,
        color=0xfce303
    )
    embed.set_footer(
        text=footer
    )
    return embed

def err_embed(error, author):
    embed = discord.Embed(
        title=f"An Error Has Occurred",
        description=error,
        color=0xff1919
    )
    embed.set_footer(
        text=f"Command By: {author}"
    )
    return embed


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["evict"])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, user: discord.Member, *, reason = None):
        if ctx.author.top_role.position > user.top_role.position:
            await user.ban(reason = reason)
            embed = com_embed(
                title=f"****{user}**** has been **BANNED**",
                description=f"Reason: {reason}",
                footer=f"Banned By: {ctx.author}"
            )
            await user.send("```You have been banned from The Peoples Republic of Banana```")
            await user.send(embed=embed)
            
        else:
            embed = err_embed(
                error=f"{ctx.author} your role is not high enough.",
                author=ctx.author
            )
        
        await ctx.channel.send(embed=embed)
        
    @commands.command(aliases=["yeet"])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, user: discord.Member, *, reason = None):
        if ctx.author.top_role.position > user.top_role.position:
            await user.kick(reason = reason)
            embed = com_embed(
                title=f"****{user}**** has been **KICKED**",
                description=f"Reason: {reason}",
                footer=f"Kicked By: {ctx.author}"
            )
            await user.send("```You have been kicked from The Peoples Republic of Banana```")
            await user.send(embed=embed)
            
        else:
            embed = err_embed(
                error=f"{ctx.author} your role is not high enough.",
                author=ctx.author
            )
        
        await ctx.channel.send(embed=embed)
        
    @commands.command(aliases=["lockdown", "panic"])
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages:
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = com_embed(
                title=f"****{channel.name}**** has been **LOCKED**",
                description=f"Channel has been locked until further notice, unless special perms apply no messages can be sent.",
                footer=f"Locked By: {ctx.author}"
            )
            
        else:
            embed = err_embed(
                error=f"{ctx.author} channel is already locked.",
                author=ctx.author
            )
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["silence", "censor"])
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member, *, reason=None):
        muted = discord.utils.get(ctx.guild.roles, name = 'Rotten Banana')
        normal = discord.utils.get(ctx.guild.roles, name = 'Banana Peasent')

        if ctx.author.top_role.position > user.top_role.position:
            await user.remove_roles(normal)
            await user.add_roles(muted)
            embed = com_embed(
                title=f"****{user}**** has been **MUTED**",
                description=f"Reason: {reason}",
                footer=f"Muted By: {ctx.author}"
            )
            await user.send("```You have been muted on The Peoples Republic of Banana```")
            await user.send(embed=embed)
            
        else:
            embed = err_embed(
                error=f"{ctx.author} your role is not high enough.",
                author=ctx.author
            )
        
        await ctx.channel.send(embed=embed)
        
    @commands.command(aliases=["slow", "slowmode"])
    @commands.has_permissions(manage_channels=True)
    async def setslow(self, ctx, seconds: int, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        await channel.edit(slowmode_delay=seconds)
        embed = com_embed(
            title=f"****{channel.name}**** slowmode has been changed",
            description=f"Channel slow mode has been set to: {seconds}",
            footer=f"Command By: {ctx.author}"
        )

        await ctx.channel.send(embed=embed)
    
    @commands.command(aliases=["pardon"])
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, user: discord.Member):
        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:
            user_ = ban_entry.user

            if user_.id == user.id:
                await ctx.guild.unban(user)
                embed = com_embed(
                    title=f"****{user}**** has been ****UNBANNED****",
                    description=f"{user} has been re-welcomed into the community.",
                    footer=f"Unbanned By: {ctx.author}"
                )
                await user.send("```Your ban has been lifted for The Peoples Republic of Banana```")
                await user.send(embed=embed)
                break
        else:
            embed = err_embed(
                error=f"{user} not found in server bans",
                author=ctx.author
            )
            
        await ctx.channel.send(embed=embed)
        
    @commands.command(aliases=["open", "calm"])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = com_embed(
            title=f"****{channel.name}**** has been ****UNLOCKED****",
            description=f"{channel.name} is no longer locked, messages can be sent by any member who is not muted.",
            footer=f"Unlocked By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
    
    @commands.command(aliases=["unsilence", "uncensor"])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        muted = discord.utils.get(ctx.guild.roles, name = 'Rotten Banana')
        normal = discord.utils.get(ctx.guild.roles, name = 'Banana Peasent')
        await user.remove_roles(muted)
        await user.add_roles(normal)
        embed = com_embed(
            title=f"****{user}**** has been **UN-MUTED**",
            description="User can now send messages and speak",
            footer=f"Un-Muted By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
        await user.send("```You have been un-muted on The Peoples Republic of Banana```")
        await user.send(embed=embed)
        return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, user: discord.Member, *, warning=None):
        data = get_user(user.id)

        if not data:
            create_user(user.id)
        
        add_warn(user.id, warning)

        embed = com_embed(
            title=f"****{user}**** has been ****WARNED****",
            description=f"Warning: {warning}",
            footer=f"Warned By: {ctx.author}"
        )
        
        await ctx.channel.send(embed=embed)
        await user.send("```You have been warned on The Peoples Republic of Banana```")
        await user.send(embed=embed)

    @commands.command(aliases=["warnings"])
    async def warns(self, ctx, user: discord.Member=None, command=None):
        user = user or ctx.author
        data = get_user(user.id)

        if not data:
            create_user(user.id)
            data = get_user(user.id)

        if command == "clear":
            if ctx.author.guild_permissions.administrator:
                warns = len(data["warns"])
                reset_warns(user.id)

                embed = com_embed(
                    title=f"{user} warns have been cleared",
                    description=f"Warns cleared: {warns}",
                    footer=f"Cleared By: {ctx.author}"
                )
                await ctx.channel.send(embed=embed)
                await user.send("```Your warns on The Peoples Republic of Banana have been cleared```")
                await user.send(embed=embed)
            else:
                embed = err_embed(
                    error=f"{ctx.author} you don't have administrator privilages",
                    author=ctx.author
                )
                await ctx.channel.send(embed=embed)

        else:
            embed = com_embed(
                title=f"{user} has {len(warns:=data['warns'])} warnings",
                description="\n".join(warns),
                footer=f"Requested By: {ctx.author}"
            )

            await ctx.channel.send(embed=embed)

    @commands.command(aliases=["clear, clean"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, qty: int=5):
        await ctx.channel.purge(limit=qty)
        embed = com_embed(
            title=f"Messages purge in {ctx.channel}",
            description=f"Messages deleted: {qty}",
            footer=f"Purge By: {ctx.author}"
        )
        msg = await ctx.channel.send(embed=embed)
        time.sleep(3)
        await msg.delete()