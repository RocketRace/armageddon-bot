import asyncio
import discord
import random

from discord.ext import commands

# For the "the" armageddon option
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

        await ctx.trigger_typing()
        warning_message = open("text/the.txt")
        await asyncio.sleep(2)
        await ctx.send(warning_message.read())
        warning_message.close()
        try:
            await self.bot.wait_for("message", timeout=45.0, check=user_accepted)
        except asyncio.TimeoutError:
            await ctx.send("In your hesitation, the word fades away... Perhaps that's for the better...")
        else:
            # Story
            await ctx.trigger_typing()
            response_message = open("text/the2.txt")
            await asyncio.sleep(1)
            await ctx.send(response_message.read())
            response_message.close()
            
            # Gets all members the bot has access to
            own_position = ctx.guild.me.top_role.position
            all_members = ctx.guild.members
            to_delete = []
            for i, member in enumerate(all_members):
                # Can't edit users with higher roles than you
                if member.top_role.position > own_position or member == ctx.guild.owner:
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
                if role.position >= own_position:
                    to_delete.append(i)
            to_delete.reverse()
            for i in to_delete:
                all_roles.pop(i)

            # Gets all emoji
            all_emoji = ctx.guild.emojis

            # Changes everybody's nickname to "the"
            for member in all_members:
                await member.edit(nick="the", reason="the")
            
            # Changes every role to "the"
            for role in all_roles:
                await role.edit(name="the", reason="the")

            # Renames every channel to "the"
            for channel in all_channels:
                # Text channels get the channel topic edited as well
                if isinstance(channel, discord.TextChannel):
                    await channel.edit(name="the", topic="the", reason="the")
                else:
                    await channel.edit(name="the", reason="the")

            # Delets every emoji 
            for emoji in all_emoji:
                # Can't edit Twitch integration emoji
                if not emoji.managed:
                    await emoji.delete()
            # Replaces them with "the"
            icon = open("images/the.png", "rb")
            for i in range(ctx.guild.emoji_limit):
                icon.seek(0)
                await ctx.guild.create_custom_emoji(name="the", image=icon.read(), reason="the")

            # Renames the guild to "the"
            # Changes the icon to "the"
            icon.seek(0)
            await ctx.guild.edit(name="the", icon=icon.read())
            icon.close()



            


def setup(bot):
    bot.add_cog(TheCog(bot))