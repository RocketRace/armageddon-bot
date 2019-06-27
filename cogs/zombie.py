import asyncio
import discord
import random

from discord.ext import commands

# For the "nuclear fallout" armageddon option
class ZombieCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def zombie(self, ctx):
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
            await self.bot.wait_for("message", timeout=30.0, check=user_accepted)
        except asyncio.TimeoutError:
            await ctx.send("Aborting...")
        else:
            await ctx.send("Here we go...")

            # Prepares roles for mass updates
            all_roles = ctx.guild.roles

            # Patches the list to ignore inaccessible roles
            own_position = ctx.guild.me.top_role.position
            to_delete = []
            for i, role in enumerate(all_roles):
                if role.position > own_position:
                    to_delete.append(i)
            to_delete.reverse()
            for i in to_delete:
                all_roles.pop(i)
            
            # Turns the roles "zombie"
            color = discord.Color(0x376640)
            permissions = discord.Permissions(permissions=66560)
            for role in all_roles:
                print(role.name + " turned into a zombie")
                # await role.edit(name="Zombie", color=color, permissions=permissions, reason="It's the end of the world!")

            # Selects text channels for the outbreak
            text_channels = [channel for channel in ctx.guild.channels if isinstance(channel, discord.TextChannel)]
            marked_channels = random.sample(text_channels, len(text_channels))

            # Starts a "zombie outbreak"
            for channel in marked_channels:
                # await channel.send(OUTBREAK_MESSAGE)

                # Gets rid of existing webhooks and makes new "zombie" ones
                existing_webhooks = await channel.webhooks()
                for webhook in existing_webhooks:
                    await webhook.delete()
                # You can have up to 10 webhooks in a channel
                zombie_webhooks = []
                zombie_avatars = [None, None, None, None, None, None, None, None, None, None] # TODO
                for i in range(10):
                    avatar = zombie_avatars[i]
                    webhook = await channel.create_webhook(name="Zombie", avatar=None, reason="It's the end of the world!")
                    zombie_webhooks.append(webhook)

                # The channel is now "infected"
                print(channel.name + " is now infected")
                # await channel.edit(name="infected", slowmode_delay=21600)
                await channel.send("A strange grumbling emanates from within the ground... Soil behins to shake.")

            zombie_messages = ["grrrr....", "Braaaains...", "Grr..", "Raawr...", "...", "zzzzzz...", "Braainz...", "RRRrrr..."]
            zombie_webhooks = {}

            # Sends up to 250 random zombie messages in total in the infected channels
            for i in range(random.randint(1, 250)):
                channel = random.choice(marked_channels)
                # Caching
                if zombie_webhooks.get(channel.id) is None:
                    zombie_webhooks[channel.id] = await channel.webhooks()
                zombie = random.choice(zombie_webhooks[channel.id])
                message = random.choice(zombie_messages)
                await zombie.send(message)
                await asyncio.sleep(0.1)




            


def setup(bot):
    bot.add_cog(ZombieCog(bot))