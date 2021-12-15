from operator import invert
import discord
from discord.ext import commands
import json
import time

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
        color=0xfce303
    )
    embed.set_footer(
        text=f"Command by: {author}"
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
                embed = discord.Embed(
                    title=f"****{user}**** has been ****UNBANNED****",
                    description=f"{user} has been re-welcomed into the community.",
                    color=0xfce303
                )
                embed.set_footer(
                    text=f"Unbanned By: {ctx.author}"
                )
                await ctx.channel.send(embed=embed)
                break;
        else:
            await ctx.channel.send("User not found in server bans")
        
    @commands.command(aliases=["open", "calm"])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(
            title=f"****{channel.name}**** has been ****UNLOCKED****",
            description=f"{channel.name} is no longer locked, messages can be sent by any member who is not muted.",
            color=0xfce303
        )
        embed.set_footer(
            text=f"Unlocked By: {ctx.author}"
        )
        await ctx.channel.send(embed=embed)
    
    @commands.command(aliases=["unsilence", "uncensor"])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        muted = discord.utils.get(ctx.guild.roles, name = 'Rotten Banana')
        normal = discord.utils.get(ctx.guild.roles, name = 'Banana Peasent')
        await user.remove_roles(muted)
        await user.add_roles(normal)
        await ctx.channel.send(f"{user.mention} has been un-muted")
        await user.send("You were un-muted")
        return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, user: discord.Member, *, warning=None):
        with open("/Users/altan/Programming/Python/Banana Bot/src/data/users.json", "r") as f:
            users = json.load(f)

        try:
            with open("/Users/altan/Programming/Python/Banana Bot/src/data/users.json", "w") as f:
                users[f"{user.id}"]["warns"].append(warning)
                json.dump(users, f, indent=2)

        except:
            with open("/Users/altan/Programming/Python/Banana Bot/src/data/users.json", "w") as f:
                users.update({f"{user.id}": {"social_credit": 0, "warns": []}})
                users[f"{user.id}"]["warns"].append(warning)
                json.dump(users, f, indent=2)
        
        await ctx.channel.send(f"{user.mention} has been warned")
        if warning:
            await user.send(f"You have been warned: {warning}")

    @commands.command(aliases=["warnings"])
    async def warns(self, ctx, i, user: discord.Member=None):
        user = user or ctx.author

        with open("/Users/altan/Programming/Python/Banana Bot/src/data/users.json", "r") as f:
            users = json.load(f)

        if i == "all":
            await ctx.channel.send(f"{user.mention} you have {len(users[f'{ctx.author.id}']['warns'])}")

        elif i == "clear":
            if ctx.author.guild_permissions.administrator:
                with open("/Users/altan/Programming/Python/Banana Bot/src/data/users.json", "w") as f:
                    users[f'{ctx.author.id}']["warns"] = []
                    json.dump(users, f, indent=2)
                await ctx.channel.send(f"{user.mention} your warns have been cleared")
            else:
                await ctx.channel.send(f"{user.mention} you don't have administrator privilages")

        else:
            try:
                await ctx.channel.send(f"{user.mention} your warning {i}: {users[f'{ctx.author.id}']['warns'][int(i)-1]}")
            except:
                pass

    @commands.command(aliases=["clear, clean"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, qty: int):
        await ctx.channel.purge(limit=qty)
        msg = await ctx.channel.send(f"{qty} messages were deleted")
        time.sleep(3)
        await msg.delete()