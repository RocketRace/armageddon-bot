import asyncio
import discord
import random

from discord.ext import commands


class UserRefused(commands.UserInputError):
    pass

# For the "nuclear fallout" armageddon option
class NuclearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nuclear(self, ctx):
        # For retaining sessions
        def user_accepted(new_ctx):
            if new_ctx.author.id != ctx.author.id:
                return False
            if new_ctx.content != "yes":
                raise UserRefused()
            return True

            # TODO throw error if the content is anything but "yes"

        warning_message = "WARNING_MESSAGE"
        await ctx.send(warning_message)
        try:
            await self.bot.wait_for("message", timeout=30.0, check=user_accepted)
        except asyncio.TimeoutError:
            await ctx.send("You do not press the button. Aborting...")
        else:
            await ctx.send("You press the button.")

            await ctx.send("You hear early warning systems kick in outside.")
        
            # Prepares the guild for nuclear strike
            all_channels = ctx.guild.channels
            all_users = ctx.guild.members

            # Absolutely nukes each channel and all users recently active in those
            random.shuffle(all_channels)
            for marked_channel in all_channels:
                marked_users = []
                # Only does something for text & voice channels
                is_text_channel = isinstance(marked_channel, discord.TextChannel)
                is_voice_channel = isinstance(marked_channel, discord.VoiceChannel)
                if is_text_channel:
                    # Sends an early warning message
                    await marked_channel.send("EARLY_WARNING_MESSAGE") 

                    # Chooses users to destroy along with the channel
                    message_history = marked_channel.history()
                    async for message in message_history:
                        if message.author not in marked_users:
                            marked_users.append(message.author)
                elif is_voice_channel:
                    # TODO: Sends a voice clip of a warning message
                    marked_users = marked_channel.members

                # Has a delay if any users are about to get kicked
                if marked_users: await asyncio.sleep(random.random() * 5)
                # Kicks every marked user
                for user in marked_users:
                    print(user.display_name)
                    # await user.kick()
                    pass
                # Deletes the channel
                print(marked_channel.name)
                # await marked_channel.delete()
            print("Done. Happy now?")

def setup(bot):
    bot.add_cog(NuclearCog(bot))