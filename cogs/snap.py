import asyncio
import discord
import random

from discord.ext import commands


class UserRefused(commands.UserInputError):
    pass

# For the "Thanos snap" armageddon option
class SnapCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def snap(self, ctx):
        # For retaining sessions
        def user_accepted(new_ctx):
            if new_ctx.author.id != ctx.author.id:
                return False
            if new_ctx.content != "yes":
                raise UserRefused()
            return True

        # Sends the warning / confirmation / story message
        await ctx.trigger_typing()
        await asyncio.sleep(2)
        warning_message = open("text/snap.txt").read()
        await ctx.send(warning_message)
        try:
            # Waits for a response
            await self.bot.wait_for("message", timeout=30.0, check=user_accepted)
        except asyncio.TimeoutError:
            await ctx.send("In your hesitation, the gauntlet suddenly dematerialized. Perhaps for the better...")
        else:
            # Story
            await ctx.trigger_typing()
            await asyncio.sleep(2)
            snap_message = open("text/snap2.txt").read()
            await ctx.send(snap_message)
            await asyncio.sleep(3)

            # Prepares channels, roles and users for deletion
            all_channels = ctx.guild.channels
            all_roles = ctx.guild.roles
            all_members = ctx.guild.members

            channel_count = len(all_channels)
            role_count = len(all_roles)
            member_count = ctx.guild.member_count

            # Cleans the member/role lists to only include members/roles the bot is able to delete
            own_role_position = ctx.guild.me.top_role.position
            to_delete = []
            for i, role in enumerate(all_roles):
                # Can't delete the @everyone role
                if role.is_default():
                    to_delete.append(i)
                # Can't delete roles above you
                elif role.position >= own_role_position:
                    to_delete.append(i)
            to_delete.reverse()
            for i in to_delete:
                all_roles.pop(i)

            to_delete.clear()
            for i, member in enumerate(all_members):
                # Can't kick users with higher roles than you
                if member.top_role.position > own_role_position:
                    to_delete.append(i)
                # You probably don't want yourself to be kicked
                elif member.id == ctx.author.id:
                    to_delete.append(i)
                # You don't want to kick the bot, since that will most likely interrupt the snap
                elif member.id == self.bot.user.id:
                    to_delete.append(i)
            to_delete.reverse()
            for i in to_delete:
                all_members.pop(i)

            # Chooses how many of each to delete (half of the total whenever possible)
            channel_delete_count = int(channel_count / 2)
            role_delete_count = int(role_count / 2)
            member_delete_count = int(member_count / 2)

            # It's not always possible to delete exactly half of everything :(
            if member_delete_count > len(all_members):
                member_delete_count = len(all_members)
            if role_delete_count > len(all_roles):
                role_delete_count = len(all_roles)

            # Chooses which ones to delete
            marked_channels = random.sample(all_channels, channel_delete_count)
            marked_roles = random.sample(all_roles, role_delete_count)
            marked_members = random.sample(all_members, member_delete_count)

            # Annihilates them one by one
            for channel in marked_channels:
                print(channel.name)
                # await channel.delete(reason="It's the end of the world!")
                await asyncio.sleep(random.random() / 5)
            for role in marked_roles:
                print(role.name)
                # await role.delete(reason="It's the end of the world!")
                await asyncio.sleep(random.random() / 5)
            for member in marked_members:
                print(member.display_name)
                # await member.kick(reason="It's the end of the world!")
                await asyncio.sleep(random.random() / 5)

            await ctx.author.send("You feel the power die down. The gauntlet turns to dust in your hands. It has been done. It is over.")


def setup(bot):
    bot.add_cog(SnapCog(bot))