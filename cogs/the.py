import asyncio
import discord
import random

from discord.ext import commands

# For the "nuclear fallout" armageddon option
class TheCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def the(self, ctx):
        # For retaining sessions
        def user_accepted(new_ctx):
            if new_ctx.author.id != ctx.author.id:
                return False
            if new_ctx.content != "yes":
                raise commands.UserInputError()
            return True

        warning_message = "WARNING_MESSAGE"
        await ctx.send(warning_message)
        try:
            await self.bot.wait_for("message", timeout=45.0, check=user_accepted)
        except asyncio.TimeoutError:
            await ctx.send("Aborting...")
        else:
            await ctx.send("Here we go...")

            # Gets all members the bot has access to
            own_position = ctx.guild.me.top_role.position
            all_members = ctx.guild.members
            to_delete = []
            for i, member in enumerate(all_members):
                # Can't edit users with higher roles than you
                if member.top_role.position > own_position:
                    to_delete.append(i)
            to_delete.reverse()
            for i in to_delete:
                all_members.pop(i)
            
            # Gets all channels
            all_channels = ctx.guild.channels

            # Gets all roles the bot has access to
            all_roles = ctx.guild.roles
            to_delete = []
            for i, role in enumerate(all_roles):
                # Can't edit roles with a higher position than you
                if role.position > own_position:
                    to_delete.append(i)
            to_delete.reverse()
            for i in to_delete:
                all_roles.pop(i)

            # Gets all emoji
            all_emoji = ctx.guild.emojis

            # Changes everybody's nickname to "the"
            for member in all_members:
                await member.edit(nick="the")
            
            # Changes every role to "the"
            for role in all_roles:
                await role.edit(name="the")

            # Renames every channel to "the"
            for channel in all_channels:
                # Text channels get the channel topic edited as well
                if isinstance(channel, discord.TextChannel):
                    await channel.edit(name="the", topic="the")
                else:
                    await channel.edit(name="the")

            # Renames every emoji to a variant of "the"
            i = 0
            for emoji in all_emoji:
                # Can't edit Twitch integration emoji
                if not emoji.managed:
                    await emoji.edit(name=f"the_{i}")
                    i += 1

            # Renames the guild to "the"
            # Changes the icon to "the"
            await ctx.guild.edit(name="the", icon=open("the.png", "rb"))



            


def setup(bot):
    bot.add_cog(TheCog(bot))